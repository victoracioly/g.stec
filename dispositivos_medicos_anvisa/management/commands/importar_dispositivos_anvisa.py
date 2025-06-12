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
        # Limpa registros anteriores (opcional, se usar banco)
        # DispositivoMedicoAnvisa.objects.all().delete()

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

        response = requests.get(link_csv, verify=False)
        if response.status_code != 200:
            self.stderr.write('❌ Falha ao baixar o CSV da Anvisa.')
            return

        df = pd.read_csv(
            BytesIO(response.content),
            sep=';', encoding='latin1', dtype=str
        )

        def limpar(valor):
            return str(valor).strip() if pd.notna(valor) else ''

        for _, row in df.iterrows():
            DispositivoMedicoAnvisa.objects.update_or_create(
                numero_registro_cadastro=limpar(
                    row.get('NUMERO_REGISTRO_CADASTRO')
                ),
                defaults={
                    'numero_processo': limpar(row.get('NUMERO_PROCESSO')),
                    'nome_tecnico': limpar(row.get('NOME_TECNICO')),
                    'classe_risco': limpar(row.get('CLASSE_RISCO')),
                    'nome_comercial': limpar(row.get('NOME_COMERCIAL')),
                    'cnpj_detentor_registro': limpar(
                        row.get('CNPJ_DETENTOR_REGISTRO_CADASTRO')
                    ),
                    'detentor_registro': limpar(
                        row.get('DETENTOR_REGISTRO_CADASTRO')
                    ),
                    'nome_fabricante': limpar(row.get('NOME_FABRICANTE')),
                    'nome_pais_fabricante': limpar(row.get('NOME_PAIS_FABRIC')),
                    # Campos DateField mantêm parse_date
                    'data_publicacao_registro': self.parse_date(
                        row.get('DT_PUB_REGISTRO_CADASTRO')
                    ),
                    # CharField: guarda texto bruto (datas ou 'VIGENTE')
                    'validade_registro': limpar(
                        row.get('VALIDADE_REGISTRO_CADASTRO')
                    ),
                    'data_atualizacao': self.parse_date(
                        row.get('DT_ATUALIZACAO_DADO')
                    ),
                }
            )

        total_linhas_csv = len(df)
        total_banco = DispositivoMedicoAnvisa.objects.count()

        self.stdout.write(
            self.style.SUCCESS('✅ Importação concluída com sucesso.')
        )
        self.stdout.write(
            self.style.WARNING(
                f'Total de linhas no CSV: {total_linhas_csv}'
            )
        )
        self.stdout.write(
            self.style.WARNING(
                f'Total de registros salvos no banco: {total_banco}'
            )
        )

    def obter_link_csv(self, pagina_url):
        resp = requests.get(pagina_url)
        soup = BeautifulSoup(resp.text, 'lxml')
        link = soup.find('a', href=re.compile(r'\.csv$', re.IGNORECASE))
        return link['href'] if link and link.has_attr('href') else None

    def parse_date(self, value):
        try:
            return pd.to_datetime(value, dayfirst=True).date() if pd.notna(value) else None
        except Exception:
            return None
