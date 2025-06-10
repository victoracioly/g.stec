from django.shortcuts import render

def home(request):
    # Simulação de dados (você pode substituir depois por dados reais)
    contexto = {
        'atas_vigentes': 12,
        'custo_equipamentos': 340000.50,
        'custo_materiais': 120000.75,
        'contratos_proximos': [
            {'numero': '2024/102', 'vencimento': '2025-06-15'},
            {'numero': '2023/215', 'vencimento': '2025-07-01'}
        ],
        'atas_pendentes': 3,
        'atas_vencidas': 5,
        'aquisicoes_mes': 18,
        'gasto_contratos': 560000.90,
        'fornecedores_ativos': 27
    }
    return render(request, 'core/home.html', contexto)
