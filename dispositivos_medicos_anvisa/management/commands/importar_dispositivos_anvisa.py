import os
import requests
import pandas as pd
from io import BytesIO
from datetime import date
from django.core.management.base import BaseCommand
from dispositivos_medicos_anvisa.models import DispositivoMedicoAnvisa


class Command(BaseCommand):
    help = 'Importa a lista de dispositivos médicos a partir de um CSV público no S3'

    def handle(self, *args, **kwargs):
        url_csv = 'https://gstec-anvisa.s3.sa-east-1.amazonaws.com/dispositivos.csv'
        self.stdout.write(f'📥 Baixando CSV diretamente do S3: {url_csv}')

        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, '..', '..', 'data')
        os.makedirs(data_dir, exist_ok=True)
        csv_path = os.path.join(data_dir, 'dispositivos_raw.csv')

        try:
            response = requests.get(url_csv, timeout=60)
            response.raise_for_status()
            with open(csv_path, 'wb') as f:
                f.write(response.content)
            csv_data = BytesIO(response.content)
        except Exception as e:
            self.stderr.write(f"⚠️ Erro ao baixar, tentando usar o último CSV salvo. {e}")
            if not os.path.exists(csv_path):
                self.stderr.write("❌ Nenhum CSV salvo encontrado.")
                return
            with open(csv_path, 'rb') as f:
                csv_data = BytesIO(f.read())

        df = pd.read_csv(
            csv_data,
            sep=';',
            encoding='latin1',
            dtype=str,
            converters={'NUMERO_REGISTRO_CADASTRO': lambda x: str(x).strip()}
        )
        df.columns = df.columns.str.strip()

        colunas_esperadas = [
            'NUMERO_REGISTRO_CADASTRO', 'NUMERO_PROCESSO', 'NOME_TECNICO',
            'CLASSE_RISCO', 'NOME_COMERCIAL', 'CNPJ_DETENTOR_REGISTRO_CADASTRO',
            'DETENTOR_REGISTRO_CADASTRO', 'NOME_FABRICANTE', 'NOME_PAIS_FABRIC',
            'DT_PUB_REGISTRO_CADASTRO', 'VALIDADE_REGISTRO_CADASTRO', 'DT_ATUALIZACAO_DADO'
        ]
        faltando = [col for col in colunas_esperadas if col not in df.columns]
        if faltando:
            self.stderr.write(f"❌ Colunas ausentes no CSV: {faltando}")
            return

        def limpar(valor):
            if pd.isna(valor) or str(valor).lower().strip() in ('nan', 'none', ''):
                return ''
            return str(valor).strip().zfill(14)

        def limpar_data(valor):
            try:
                if not valor or "00/00" in valor or str(valor).lower() in ("n/a", "nan", "vigente"):
                    return date(3000, 1, 1)
                dt = pd.to_datetime(valor, format="%m/%d/%Y %H:%M:%S", errors="coerce")
                if pd.isna(dt) or dt is pd.NaT:
                    return date(3000, 1, 1)
                return dt.date()
            except Exception:
                return date(3000, 1, 1)

        registros_sucesso = 0
        registros_erro = 0

        with open('log_erros_importacao.txt', 'w', encoding='utf-8') as log_file:
            log_file.write("LOG DE ERROS DE IMPORTAÇÃO\n\n")

        for idx, row in df.iterrows():
            if idx % 100 == 0:
                self.stdout.write(f"🔄 Processando linha {idx}/{len(df)}...")

            try:
                numero = limpar(row.get('NUMERO_REGISTRO_CADASTRO'))

                if not numero:
                    registros_erro += 1
                    mensagem_erro = f"⚠️ Linha {idx} ignorada - Número de registro vazio ou inválido.\n"
                    self.stderr.write(mensagem_erro)
                    with open('log_erros_importacao.txt', 'a', encoding='utf-8') as log_file:
                        log_file.write(mensagem_erro)
                    continue

                DispositivoMedicoAnvisa.objects.update_or_create(
                    numero_registro_cadastro=numero,
                    defaults={
                        'numero_processo': limpar(row.get('NUMERO_PROCESSO')),
                        'nome_tecnico': limpar(row.get('NOME_TECNICO')),
                        'classe_risco': limpar(row.get('CLASSE_RISCO')),
                        'nome_comercial': limpar(row.get('NOME_COMERCIAL')),
                        'cnpj_detentor_registro': limpar(row.get('CNPJ_DETENTOR_REGISTRO_CADASTRO')),
                        'detentor_registro': limpar(row.get('DETENTOR_REGISTRO_CADASTRO')),
                        'nome_fabricante': limpar(row.get('NOME_FABRICANTE')),
                        'nome_pais_fabricante': limpar(row.get('NOME_PAIS_FABRIC')),
                        'data_publicacao_registro': limpar_data(row.get('DT_PUB_REGISTRO_CADASTRO')),
                        'validade_registro': limpar(row.get('VALIDADE_REGISTRO_CADASTRO')),
                        'data_atualizacao': limpar_data(row.get('DT_ATUALIZACAO_DADO')),
                    }
                )
                registros_sucesso += 1
            except Exception as e:
                registros_erro += 1
                mensagem_erro = f"⚠️ Erro na linha {idx} - Registro {row.get('NUMERO_REGISTRO_CADASTRO')}: {e}\n"
                self.stderr.write(mensagem_erro)
                with open('log_erros_importacao.txt', 'a', encoding='utf-8') as log_file:
                    log_file.write(mensagem_erro)

        total_linhas_csv = len(df)
        total_banco = DispositivoMedicoAnvisa.objects.count()

        self.stdout.write(self.style.SUCCESS('✅ Importação concluída com sucesso.'))
        self.stdout.write(self.style.WARNING(f'Total de linhas no CSV: {total_linhas_csv}'))
        self.stdout.write(self.style.WARNING(f'Total de registros salvos no banco: {total_banco}'))
        self.stdout.write(self.style.SUCCESS(f'✅ Registros salvos com sucesso: {registros_sucesso}'))
        self.stdout.write(self.style.ERROR(f'❌ Registros com erro: {registros_erro} (ver log_erros_importacao.txt)'))
        self.stdout.write(self.style.SUCCESS(f'Total processado no loop: {registros_sucesso + registros_erro}'))
