import requests
from datetime import datetime

API_CONTRATACOES_URL = "https://pncp.gov.br/api/consulta/v1/contratacoes/publicacao"
API_ATAS_URL = "https://pncp.gov.br/api/consulta/v1/atas"

# ✅ Função para buscar Atas
def buscar_atas_pncp(data_inicial, data_final, cnpj=None, codigo_ua=None, max_paginas=5):
    url = API_ATAS_URL
    pagina = 1
    total_atas = []

    print(f"[BUSCA] Iniciando busca de atas para o período: {data_inicial} - {data_final}")

    while pagina <= max_paginas:
        params = {
            "dataInicial": data_inicial,
            "dataFinal": data_final,
            "pagina": str(pagina)
        }

        if cnpj:
            params["cnpj"] = cnpj

        if codigo_ua:
            params["codigoUnidadeAdministrativa"] = codigo_ua

        try:
            response = requests.get(url, params=params, headers={
                "accept": "application/json",
                "User-Agent": "Mozilla/5.0"
            }, timeout=10)

            if response.status_code == 200:
                data = response.json()
                atas = data.get('data', [])

                if not atas:
                    print(f"[INFO] Não há mais atas na página {pagina}. Finalizando busca.")
                    break

                total_atas.extend(atas)  # ✅ Adicionei todos de uma vez para melhorar performance
                pagina += 1
            else:
                print(f"[ERRO] Status Code {response.status_code}: {response.text}")
                break

        except Exception as e:
            print(f"[ERRO] Falha na conexão com a API: {e}")
            break

    print(f"[BUSCA] Total de atas encontradas: {len(total_atas)}")
    return total_atas


# ✅ Função para buscar Contratações (SEM LIMITE DE PÁGINAS, SOMENTE UASG ESPECÍFICA)
def buscar_contratacoes_pncp(data_inicial, data_final, cnpj, codigo_ua, modalidade=None):
    url = API_CONTRATACOES_URL
    pagina = 1
    total_contratacoes = []

    print(f"[BUSCA] Iniciando busca de contratações para a UASG {codigo_ua} - CNPJ {cnpj} no período: {data_inicial} - {data_final}")

    while True:
        params = {
            "dataInicial": data_inicial,
            "dataFinal": data_final,
            "cnpj": cnpj,
            "codigoUnidadeAdministrativa": codigo_ua,
            "pagina": str(pagina)
        }

        if modalidade:
            params["codigoModalidadeContratacao"] = modalidade

        try:
            response = requests.get(url, params=params, headers={
                "accept": "application/json",
                "User-Agent": "Mozilla/5.0"
            }, timeout=10)

            if response.status_code == 200:
                data = response.json()
                contratacoes = data.get('data', [])

                if not contratacoes:
                    print(f"[INFO] Não há mais contratações na página {pagina}. Finalizando busca.")
                    break

                total_contratacoes.extend(contratacoes)  # ✅ Adicionei todos de uma vez para melhorar performance
                pagina += 1
            else:
                print(f"[ERRO] Status Code {response.status_code}: {response.text}")
                break

        except Exception as e:
            print(f"[ERRO] Falha na conexão com a API: {e}")
            break

    print(f"[BUSCA] Total de contratações encontradas: {len(total_contratacoes)}")
    return total_contratacoes
