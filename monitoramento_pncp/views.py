from django.shortcuts import render
from django.core.paginator import Paginator
from .integracao_pncp import buscar_atas_pncp, buscar_contratacoes_pncp
from datetime import datetime
from urllib.parse import unquote
from django.http import Http404

#  Dicionário para converter códigos em nomes de modalidades
MODALIDADES = {
    "1": "Leilão - Eletrônico",
    "2": "Diálogo Competitivo",
    "3": "Concurso",
    "4": "Concorrência - Eletrônica",
    "5": "Concorrência - Presencial",
    "6": "Pregão - Eletrônico",
    "7": "Pregão - Presencial",
    "8": "Dispensa de Licitação",
    "9": "Inexigibilidade",
    "10": "Manifestação de Interesse",
    "11": "Pré-qualificação",
    "12": "Credenciamento",
    "13": "Leilão - Presencial"
}

# ============================================
#  MONITORAMENTO DE ATAS
# ============================================
def monitoramento_atas_pncp(request):
    print("[DEBUG] ➡️ Entrou na view monitoramento_atas_pncp")

    #  Parâmetros opcionais de busca
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')
    cnpj = request.GET.get('cnpj', None)
    codigo_ua = request.GET.get('codigo_ua', None)

    #  Definindo datas padrão, se não informadas
    if not data_inicial:
        data_inicial = f"{datetime.now().year}-01-01"
    if not data_final:
        data_final = f"{datetime.now().year}-12-31"

    print(f"[DEBUG] ➡️ Datas para busca: Inicial = {data_inicial}, Final = {data_final}")

    #  Formatação das datas
    try:
        data_inicial_formatada = datetime.strptime(data_inicial, '%Y-%m-%d').strftime('%Y%m%d')
        data_final_formatada = datetime.strptime(data_final, '%Y-%m-%d').strftime('%Y%m%d')
    except ValueError as e:
        print(f"[ERRO] ➡️ Formato de data inválido: {e}")
        data_inicial_formatada = '20230101'
        data_final_formatada = '20231231'

    #  Paginação e Busca
    try:
        atas_pncp = buscar_atas_pncp(data_inicial_formatada, data_final_formatada, cnpj, codigo_ua)
        paginator = Paginator(atas_pncp, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        request.session['atas_pncp'] = atas_pncp
    except Exception as e:
        print(f"[ERRO] ➡️ Falha ao buscar atas: {e}")
        page_obj = []

    context = {
        'page_obj': page_obj,
        'data_inicial': data_inicial,
        'data_final': data_final,
        'atas': atas_pncp
    }

    return render(request, 'monitoramento_pncp/monitoramento_atas_pncp.html', context)


# ============================================
#  MONITORAMENTO DE CONTRATAÇÕES
# ============================================
def monitoramento_contratacoes_pncp(request):
    print("[DEBUG] ➡️ Entrou na view monitoramento_contratacoes_pncp")

    # 🔹 Parâmetros opcionais de busca
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')
    cnpj = request.GET.get('cnpj', "15126437000143")
    codigo_ua = request.GET.get('codigo_ua', "155007")
    modalidade = request.GET.get('modalidade', None)

    # 🔹 Definindo datas padrão, se não informadas
    if not data_inicial:
        data_inicial = f"{datetime.now().year}-01-01"
    if not data_final:
        data_final = f"{datetime.now().year}-12-31"

    print(f"[DEBUG] ➡️ Datas para busca: Inicial = {data_inicial}, Final = {data_final}")
    print(f"[DEBUG] ➡️ CNPJ informado: {cnpj}")
    print(f"[DEBUG] ➡️ Código UASG informado: {codigo_ua}")

    # 🔹 Formatação das datas
    try:
        data_inicial_formatada = datetime.strptime(data_inicial, '%Y-%m-%d').strftime('%Y%m%d')
        data_final_formatada = datetime.strptime(data_final, '%Y-%m-%d').strftime('%Y%m%d')
    except ValueError as e:
        print(f"[ERRO] ➡️ Formato de data inválido: {e}")
        data_inicial_formatada = '20230101'
        data_final_formatada = '20231231'

    # 🔹 Paginação e Busca
    try:
        contratacoes_pncp = buscar_contratacoes_pncp(data_inicial_formatada, data_final_formatada, cnpj, codigo_ua, modalidade)

        # ✅ Ordenação pela data de atualização (mais recente primeiro)
        contratacoes_pncp.sort(key=lambda x: x.get('dataAtualizacao'), reverse=True)

        # ✅ Garantindo que a data esteja formatada
        for item in contratacoes_pncp:
            data_atualizacao = item.get('dataAtualizacao')
            if data_atualizacao:
                item['dataAtualizacaoFormatada'] = datetime.strptime(data_atualizacao, "%Y-%m-%dT%H:%M:%S").strftime("%d/%m/%Y %H:%M")

        paginator = Paginator(contratacoes_pncp, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        request.session['contratacoes_pncp'] = contratacoes_pncp

    except Exception as e:
        print(f"[ERRO] ➡️ Falha ao buscar contratações: {e}")
        page_obj = []

    context = {
        'page_obj': page_obj,
        'data_inicial': data_inicial,
        'data_final': data_final,
        'codigo_ua': codigo_ua,
        'cnpj': cnpj,
        'modalidade': modalidade,
        'contratacoes': contratacoes_pncp,
        'MODALIDADES': MODALIDADES
    }

    return render(request, 'monitoramento_pncp/monitoramento_contratacoes_pncp.html', context)


# ============================================
# 🚀 DETALHES DA ATA
# ============================================
def detalhes_atas_pncp(request, numeroControle):
    numeroControle = unquote(numeroControle)
    atas_pncp = request.session.get('atas_pncp', [])
    ata_detalhes = next((ata for ata in atas_pncp if ata.get('numeroControlePNCPAta') == numeroControle), None)

    if not ata_detalhes:
        context = {'mensagem': "Ata não encontrada."}
        return render(request, 'monitoramento_pncp/erro_ata_nao_encontrada.html', context)

    context = {'ata': ata_detalhes}
    return render(request, 'monitoramento_pncp/detalhes_atas_pncp.html', context)


# ============================================
#  DETALHES DA CONTRATAÇÃO
# ============================================
def detalhes_contratacao_pncp(request, numeroContrato):
    numeroContrato = unquote(numeroContrato)
    contratacoes_pncp = request.session.get('contratacoes_pncp', [])
    contratacao_detalhes = next((c for c in contratacoes_pncp if c.get('numeroControlePNCP') == numeroContrato), None)

    if not contratacao_detalhes:
        raise Http404("Contratação não encontrada.")

    context = {'contratacao': contratacao_detalhes}
    return render(request, 'monitoramento_pncp/detalhes_contratacoes_pncp.html', context)
