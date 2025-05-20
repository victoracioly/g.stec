import requests

url = "https://pncp.gov.br/api/consulta/v1/pca/usuario"
params = {
    "anoPca": 2023,
    "idUsuario": 3,
    "pagina": 1
}

headers = {
    "accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://pncp.gov.br",
    "Origin": "https://pncp.gov.br",
}

response = requests.get(url, params=params, headers=headers, timeout=10)

print("Content-Type:", response.headers.get('Content-Type'))
print("Conteúdo bruto:\n", response.text[:500])

try:
    json_data = response.json()
    print("\n✅ Resposta é um JSON válido!")
    print(json_data)
except ValueError as e:
    print("\n❌ A resposta não é um JSON válido.")
