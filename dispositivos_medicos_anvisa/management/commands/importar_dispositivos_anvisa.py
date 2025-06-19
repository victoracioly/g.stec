import os
import requests
import pandas as pd
from io import BytesIO
from django.core.management.base import BaseCommand
from dispositivos_medicos_anvisa.models import DispositivoMedicoAnvisa


class Command(BaseCommand):
    help = 'Importa a lista de dispositivos médicos a partir de um CSV público no S3'

    def handle(self, *args, **kwargs):
        url_csv = 'https://gstec-anvisa.s3.sa-east-1.amazonaws.com/dispositivos.csv'
        self.stdout.write(f'📥 Baixando CSV diretamente do S3: {url_csv}')

        # Caminho do CSV salvo localmente
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

        df = pd.read_csv(csv_data, sep=';', encoding='latin1', dtype=str)
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
            return str(valor).strip() if pd.notna(valor) else ''

        def limpar_data(valor):
            if not valor or "00/00" in valor or valor.lower() in ("n/a", "nan"):
                return None
            return self.parse_date(valor)

        for idx, row in df.iterrows():
            if idx % 1000 == 0:
                self.stdout.write(f"🔄 Processando linha {idx}/{len(df)}...")

            try:
                DispositivoMedicoAnvisa.objects.update_or_create(
                    numero_registro_cadastro=limpar(row.get('NUMERO_REGISTRO_CADASTRO')),
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
            except Exception as e:
                self.stderr.write(f"⚠️ Erro na linha {idx}: {e}")

        total_linhas_csv = len(df)
        total_banco = DispositivoMedicoAnvisa.objects.count()

        self.stdout.write(self.style.SUCCESS('✅ Importação concluída com sucesso.'))
        self.stdout.write(self.style.WARNING(f'Total de linhas no CSV: {total_linhas_csv}'))
        self.stdout.write(self.style.WARNING(f'Total de registros salvos no banco: {total_banco}'))

    # def parse_date(self, value):
    #     try:
    #         data = pd.to_datetime(value, format="%d/%m/%Y", errors="coerce")
    #         return data.date() if pd.notna(data) else None
    #     except Exception:
    #         return None

    def parse_date(self, value):
        try:
            return pd.to_datetime(value, format="%m/%d/%Y %H:%M:%S", errors="coerce").date() if pd.notna(
                value) else None
        except Exception:
            return None