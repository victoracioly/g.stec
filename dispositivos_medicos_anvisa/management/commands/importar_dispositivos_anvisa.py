import os
import requests
import pandas as pd
from io import BytesIO
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from dispositivos_medicos_anvisa.models import DispositivoMedicoAnvisa
import re

class Command(BaseCommand):
    help = 'Importa a lista de dispositivos médicos da Anvisa'

    def handle(self, *args, **kwargs):
        print('🔗 Obtendo link CSV')
        url_pagina = (
            'https://www.gov.br/anvisa/pt-br/assuntos/produtosparasaude/'
            'lista-de-dispositivos-medicos-regularizados'
        )
        link_csv = self.obter_link_csv(url_pagina)
        if not link_csv:
            self.stderr.write('❌ Link CSV não encontrado.')
            return
        self.stdout.write(f'✅ Link CSV encontrado: {link_csv}')

        # Caminho do CSV salvo localmente
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, '..', '..', 'data')
        os.makedirs(data_dir, exist_ok=True)
        csv_path = os.path.join(data_dir, 'dispositivos_raw.csv')

        # Baixa o CSV
        try:
            response = requests.get(link_csv, verify=False, timeout=60)
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

        # Lê e limpa o CSV
        df = pd.read_csv(
            csv_data,
            sep=';', encoding='latin1', dtype=str, errors='replace'
        )
        df.columns = df.columns.str.strip()  # Remove espaços nos nomes das colunas

        # Verifica se todas as colunas esperadas estão presentes
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

        for _, row in df.iterrows():
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
                    'data_publicacao_registro': self.parse_date(limpar(row.get('DT_PUB_REGISTRO_CADASTRO'))),
                    'validade_registro': limpar(row.get('VALIDADE_REGISTRO_CADASTRO')),
                    'data_atualizacao': self.parse_date(limpar(row.get('DT_ATUALIZACAO_DADO'))),
                }
            )

        total_linhas_csv = len(df)
        total_banco = DispositivoMedicoAnvisa.objects.count()

        self.stdout.write(self.style.SUCCESS('✅ Importação concluída com sucesso.'))
        self.stdout.write(self.style.WARNING(f'Total de linhas no CSV: {total_linhas_csv}'))
        self.stdout.write(self.style.WARNING(f'Total de registros salvos no banco: {total_banco}'))

    def obter_link_csv(self, pagina_url):
        try:
            resp = requests.get(pagina_url, timeout=30)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'lxml')
            link = soup.find('a', href=re.compile(r'\.csv$', re.IGNORECASE))
            return link['href'] if link and link.has_attr('href') else None
        except Exception as e:
            self.stderr.write(f"❌ Erro ao acessar a página da Anvisa: {e}")
            return None

    def parse_date(self, value):
        try:
            return pd.to_datetime(value, dayfirst=True).date() if pd.notna(value) else None
        except Exception:
            return None
