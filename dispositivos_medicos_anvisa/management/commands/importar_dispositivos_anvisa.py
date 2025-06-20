# Importa bibliotecas necessárias
import os
import requests
import pandas as pd
from io import BytesIO
from datetime import date, datetime
from django.core.management.base import BaseCommand
from dispositivos_medicos_anvisa.models import DispositivoMedicoAnvisa
from django.db import transaction


class Command(BaseCommand):
    help = 'Importa a lista de dispositivos médicos a partir de um CSV público no S3'

    def handle(self, *args, **kwargs):
        url_csv = 'https://gstec-anvisa.s3.sa-east-1.amazonaws.com/dispositivos.csv'
        self.stdout.write(f'📅 Baixando CSV diretamente do S3: {url_csv}')

        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, '..', '..', 'data')
        os.makedirs(data_dir, exist_ok=True)
        csv_path = os.path.join(data_dir, 'dispositivos_raw.csv')

        csv_data = None
        try:
            response = requests.get(url_csv, timeout=60)
            response.raise_for_status()  # Lança um erro para status HTTP ruins (4xx, 5xx)
            with open(csv_path, 'wb') as f:
                f.write(response.content)
            csv_data = BytesIO(response.content)
            self.stdout.write('✅ Download realizado com sucesso.')
        except Exception as e:
            self.stderr.write(f"⚠️ Erro ao baixar, tentando usar o último CSV salvo. {e}")
            if not os.path.exists(csv_path):
                self.stderr.write("❌ Nenhum CSV salvo encontrado. Não é possível prosseguir.")
                return  # Interrompe a execução se não houver CSV
            with open(csv_path, 'rb') as f:
                csv_data = BytesIO(f.read())
            self.stdout.write('✅ Usando CSV salvo localmente.')

        if csv_data is None:  # Garante que temos dados para processar
            self.stderr.write("❌ Não foi possível obter dados do CSV de nenhuma fonte.")
            return

        try:
            # Ao ler o CSV, já podemos usar converters para algumas colunas
            df = pd.read_csv(
                csv_data,
                sep=';',
                encoding='latin1',
                dtype=str,  # Lemos tudo como string para ter controle total na limpeza
                converters={'NUMERO_REGISTRO_CADASTRO': lambda x: str(x).strip()}
            )
            self.stdout.write(f'✅ CSV lido com sucesso. Total de linhas: {len(df)}')
        except Exception as e:
            self.stderr.write(f'❌ Erro ao ler o CSV: {e}')
            return

        df.columns = df.columns.str.strip()  # Remove espaços dos nomes das colunas
        colunas_esperadas = [
            'NUMERO_REGISTRO_CADASTRO', 'NUMERO_PROCESSO', 'NOME_TECNICO',
            'CLASSE_RISCO', 'NOME_COMERCIAL', 'CNPJ_DETENTOR_REGISTRO_CADASTRO',
            'DETENTOR_REGISTRO_CADASTRO', 'NOME_FABRICANTE', 'NOME_PAIS_FABRIC',
            'DT_PUB_REGISTRO_CADASTRO', 'VALIDADE_REGISTRO_CADASTRO', 'DT_ATUALIZACAO_DADO'
        ]

        # Verifica se todas as colunas esperadas estão presentes
        faltando = [col for col in colunas_esperadas if col not in df.columns]
        if faltando:
            self.stderr.write(f"❌ Erro: Colunas ausentes no CSV: {', '.join(faltando)}")
            return

        # --- Funções de Limpeza Otimizadas para Pandas Series ---
        def limpar_str_serie(serie):
            # Converte para string, remove espaços em branco e trata valores vazios/NaN
            return serie.fillna('').astype(str).str.strip()

        def limpar_numero_registro_serie(serie):
            # Aplica zfill após a limpeza básica de string, garantindo 14 dígitos
            return serie.fillna('').astype(str).str.strip().str.zfill(14)

        def limpar_data_serie(serie):
            # 1. Trata valores que são intrinsecamente "nulos" ou problemáticos
            serie_processada = serie.astype(str).str.lower().str.strip().replace(
                ["00/00", "n/a", "nan", "vigente", ""], pd.NaT
            )

            # 2. Tenta converter para datetime, com errors=coerce para transformar falhas em NaT
            # Tenta primeiro o formato com horas, depois inferência com dayfirst=True
            converted_dates = pd.to_datetime(serie_processada, format="%m/%d/%Y %H:%M:%S", errors="coerce")

            # Para os que ainda são NaT após a primeira tentativa, tenta com dayfirst=True
            mask_nat = pd.isna(converted_dates)
            converted_dates.loc[mask_nat] = pd.to_datetime(serie_processada.loc[mask_nat], errors="coerce",
                                                           dayfirst=True)

            # 3. Garante que todos os NaT são preenchidos com a data padrão e convertidos para datetime.date
            # Isso é CRÍTICO para evitar o erro NaTType
            final_dates = converted_dates.fillna(date(3000, 1, 1))

            # Converte para datetime.date, pois o DateField do Django espera isso.
            return final_dates.dt.date

        self.stdout.write('✨ Aplicando funções de limpeza e padronização ao DataFrame...')

        # Aplica a limpeza para o número de registro
        df['NUMERO_REGISTRO_CADASTRO'] = limpar_numero_registro_serie(df['NUMERO_REGISTRO_CADASTRO'])

        # APLICA A LIMPEZA DE DATA APENAS PARA OS CAMPOS QUE SÃO DateField NO SEU MODELO
        df['DT_PUB_REGISTRO_CADASTRO'] = limpar_data_serie(df['DT_PUB_REGISTRO_CADASTRO'])
        df['DT_ATUALIZACAO_DADO'] = limpar_data_serie(df['DT_ATUALIZACAO_DADO'])

        # O campo 'VALIDADE_REGISTRO_CADASTRO' é CharField no seu models.py,
        # então ele deve ser limpo como uma string.
        df['VALIDADE_REGISTRO_CADASTRO'] = limpar_str_serie(df['VALIDADE_REGISTRO_CADASTRO'])

        # Aplica limpeza genérica para as demais colunas de texto esperadas
        for col in colunas_esperadas:
            # Exclui as colunas já tratadas (NUMERO_REGISTRO_CADASTRO, e as 3 colunas de data/string)
            if col not in ['NUMERO_REGISTRO_CADASTRO', 'DT_PUB_REGISTRO_CADASTRO', 'DT_ATUALIZACAO_DADO',
                           'VALIDADE_REGISTRO_CADASTRO']:
                df[col] = limpar_str_serie(df[col])

        self.stdout.write('✅ Limpeza do DataFrame concluída.')

        registros_sucesso_preparacao = 0  # Conta quantos objetos foram preparados com sucesso do CSV
        registros_erro_preparacao = 0  # Conta erros na fase de preparação do objeto
        objetos_para_inserir = []

        log_erros_path = 'log_erros_importacao.txt'
        with open(log_erros_path, 'w', encoding='utf-8') as log_file:
            log_file.write("LOG DE ERROS DE IMPORTAÇÃO\n\n")

            self.stdout.write('🔄 Preparando objetos do Django a partir do DataFrame...')
            for idx, row in df.iterrows():
                # Reduz a frequência do log de progresso para grandes datasets
                if idx % 5000 == 0:
                    self.stdout.write(f"🔄 Processando linha {idx}/{len(df)}...")

                numero = row['NUMERO_REGISTRO_CADASTRO']
                if not numero or numero.strip() == '':  # Verifica se o número de registro está vazio após a limpeza
                    registros_erro_preparacao += 1
                    msg = f"⚠️ Linha {idx} ignorada - Número de registro vazio após limpeza. Conteúdo: {row.to_dict()}\n"
                    self.stderr.write(msg)
                    log_file.write(msg)
                    continue

                try:
                    # Cria a instância do modelo DispositivoMedicoAnvisa com os dados já limpos
                    obj = DispositivoMedicoAnvisa(
                        numero_registro_cadastro=numero,
                        numero_processo=row['NUMERO_PROCESSO'],
                        nome_tecnico=row['NOME_TECNICO'],
                        classe_risco=row['CLASSE_RISCO'],
                        nome_comercial=row['NOME_COMERCIAL'],
                        cnpj_detentor_registro=row['CNPJ_DETENTOR_REGISTRO_CADASTRO'],
                        detentor_registro=row['DETENTOR_REGISTRO_CADASTRO'],
                        nome_fabricante=row['NOME_FABRICANTE'],
                        nome_pais_fabricante=row['NOME_PAIS_FABRIC'],
                        data_publicacao_registro=row['DT_PUB_REGISTRO_CADASTRO'],
                        validade_registro=row['VALIDADE_REGISTRO_CADASTRO'],  # Já limpo pelo pandas
                        data_atualizacao=row['DT_ATUALIZACAO_DADO'],  # Já limpo pelo pandas
                    )
                    objetos_para_inserir.append(obj)
                    registros_sucesso_preparacao += 1  # Contabiliza aqui para objetos válidos preparados
                except Exception as e:
                    registros_erro_preparacao += 1
                    msg = f"❌ Erro ao preparar objeto da linha {idx} - Registro '{numero}': {e}\n"
                    self.stderr.write(msg)
                    log_file.write(msg)

        self.stdout.write('📦 Salvando objetos no banco de dados em massa...')

        registros_criados_db = 0
        registros_atualizados_db = 0
        registros_erro_db = 0  # Contabiliza erros durante a operação de banco de dados em massa

        # --- Operações de Banco de Dados em Massa (Transação Atômica) ---
        with transaction.atomic():
            # Consulta todos os números de registro existentes no banco de dados
            existing_numbers = set(DispositivoMedicoAnvisa.objects.values_list('numero_registro_cadastro', flat=True))

            to_create = []
            to_update = []

            # Separa os objetos preparados entre os que precisam ser criados e os que precisam ser atualizados
            for obj in objetos_para_inserir:
                if obj.numero_registro_cadastro in existing_numbers:
                    to_update.append(obj)
                else:
                    to_create.append(obj)

            if to_create:
                try:
                    # Cria novos registros em massa. ignore_conflicts=False para lançar erro se houver duplicata inesperada.
                    created_objects = DispositivoMedicoAnvisa.objects.bulk_create(to_create, ignore_conflicts=False)
                    registros_criados_db = len(created_objects)
                    self.stdout.write(f'✅ {registros_criados_db} novos registros criados.')
                except Exception as e:
                    registros_erro_db += len(to_create)  # Todos esses falharam
                    msg = f"❌ Erro em massa ao criar registros: {e}\n"
                    self.stderr.write(msg)
                    log_file.write(msg)

            if to_update:
                # Define os campos que devem ser atualizados em massa
                update_fields = [
                    'numero_processo', 'nome_tecnico', 'classe_risco', 'nome_comercial',
                    'cnpj_detentor_registro', 'detentor_registro', 'nome_fabricante',
                    'nome_pais_fabricante', 'data_publicacao_registro', 'validade_registro',
                    'data_atualizacao'
                ]
                try:
                    updated_count = DispositivoMedicoAnvisa.objects.bulk_update(to_update, update_fields)
                    registros_atualizados_db = updated_count
                    self.stdout.write(f'✅ {registros_atualizados_db} registros atualizados.')
                except Exception as e:
                    registros_erro_db += len(to_update)  # Todos esses falharam
                    msg = f"❌ Erro em massa ao atualizar registros: {e}\n"
                    self.stderr.write(msg)
                    log_file.write(msg)

        self.stdout.write(f'✅ Operações de banco de dados concluídas.')

        total_linhas_csv = len(df)
        total_banco = DispositivoMedicoAnvisa.objects.count()

        # Agora, a contagem final é mais clara
        total_processado_com_sucesso_db = registros_criados_db + registros_atualizados_db
        total_erros_geral = registros_erro_preparacao + registros_erro_db

        self.stdout.write(self.style.SUCCESS('✅ Importação finalizada.'))
        self.stdout.write(self.style.WARNING(f'Total de linhas no CSV lido: {total_linhas_csv}'))
        self.stdout.write(self.style.WARNING(f'Total de registros no banco de dados: {total_banco}'))
        self.stdout.write(
            self.style.SUCCESS(f'✅ Registros criados/atualizados no DB: {total_processado_com_sucesso_db}'))
        self.stdout.write(self.style.ERROR(f'❌ Registros com erro (total): {total_erros_geral} (ver {log_erros_path})'))
        self.stdout.write(self.style.SUCCESS(
            f'Total de linhas do CSV tentadas (pré-processamento): {registros_sucesso_preparacao + registros_erro_preparacao}'))