# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Dashboard, Hospital
from gestaodeatas.models import AtaRegistroPreco  
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from .forms import HospitalForm

# ===========================
# 🔹 1️⃣ Geração de PDF (Relatório CEO)
# ===========================
def gerar_pdf_ceo(request):
    """
    Gera um PDF com a listagem de atas homologadas.
    """
    search = request.GET.get('search')
    hospital = request.GET.get('hospital')
    
    atas = AtaRegistroPreco.objects.filter(status='Homologada')

    if search:
        atas = atas.filter(numero_ata__icontains=search)

    if hospital:
        atas = atas.filter(hospital__icontains=hospital)

    template_path = 'users/relatorio_ceo.html'
    context = {'atas': atas}
    html = render_to_string(template_path, context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_atas.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    return response


# ===========================
# 🔹 2️⃣ View de Redirecionamento (Escolhe o Dashboard)
# ===========================
def redirecionar_dashboard(request):
    """
    Verifica o usuário logado e redireciona para o dashboard correto.
    """
    if not request.user.is_authenticated:
        return redirect('/admin/login/')
    
    try:
        dashboard = Dashboard.objects.get(usuario=request.user)
        if dashboard.role == 'STEC':
            return redirect('dashboard_stec')
        elif dashboard.role == 'SEC':
            return redirect('dashboard_sec')
        elif dashboard.role == 'CEO':
            return redirect('dashboard_ceo')
    except Dashboard.DoesNotExist:
        return redirect('/admin/')
    return redirect('/admin/')


# ===========================
# 🔹 3️⃣ Views dos Dashboards
# ===========================
def dashboard_stec(request):
    """
    Dashboard para o perfil STEC - Visualiza apenas Atas da UASG vinculada.
    """
    try:
        dashboard = Dashboard.objects.get(usuario=request.user)
        atas = AtaRegistroPreco.objects.filter(uasg=dashboard.uasg)
    except Dashboard.DoesNotExist:
        atas = []

    context = {
        'atas': atas,
        'uasg': dashboard.uasg if dashboard else 'UASG não definida'
    }
    return render(request, 'users/dashboard_stec.html', context)


def dashboard_sec(request):
    """
    Dashboard para o perfil SEC - Visualiza todas as atas da rede EBSERH.
    """
    atas = AtaRegistroPreco.objects.all()
    context = {
        'atas': atas
    }
    return render(request, 'users/dashboard_sec.html', context)


def dashboard_ceo(request):
    """
    Dashboard para o perfil CEO - Visualiza apenas as Atas Homologadas.
    Permite filtrar por Número da Ata e por Hospital.
    """
    search = request.GET.get('search')
    hospital = request.GET.get('hospital')
    
    atas = AtaRegistroPreco.objects.filter(status='Homologada')

    if search:
        atas = atas.filter(numero_ata__icontains=search)

    if hospital:
        atas = atas.filter(hospital__icontains=hospital)

    context = {
        'atas': atas
    }
    return render(request, 'users/dashboard_ceo.html', context)


# ===========================
# 🔹 4️⃣ Views para o Sidebar (Lista de Atas e Monitoramento PNCP)
# ===========================
def lista_atas(request):
    """
    Exibe a lista completa de Atas para visualização.
    """
    atas = AtaRegistroPreco.objects.all()
    return render(request, 'gestaodeatas/lista_atas.html', {'atas': atas})


def monitoramento_pncp(request):
    """
    Exibe o monitoramento do PNCP, com filtros de busca.
    """
    search = request.GET.get('search')
    uasg = request.GET.get('uasg')
    
    atas = AtaRegistroPreco.objects.all()

    if search:
        atas = atas.filter(numero_ata__icontains=search)

    if uasg:
        atas = atas.filter(uasg__icontains=uasg)

    context = {
        'atas': atas
    }
    return render(request, 'gestaodeatas/monitoramento_pncp.html', context)


# ===========================
# 🔹 5️⃣ CRUD de Hospital
# ===========================
def listar_hospitais(request):
    """
    Lista todos os hospitais cadastrados.
    """
    hospitais = Hospital.objects.all()
    return render(request, 'users/lista_hospitais.html', {'hospitais': hospitais})


def criar_hospital(request):
    """
    Cadastra um novo hospital.
    """
    if request.method == 'POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_hospitais')
    else:
        form = HospitalForm()
    
    return render(request, 'users/form_hospital.html', {'form': form})


def editar_hospital(request, hospital_id):
    """
    Edita um hospital existente.
    """
    hospital = get_object_or_404(Hospital, id=hospital_id)
    if request.method == 'POST':
        form = HospitalForm(request.POST, instance=hospital)
        if form.is_valid():
            form.save()
            return redirect('listar_hospitais')
    else:
        form = HospitalForm(instance=hospital)

    return render(request, 'users/form_hospital.html', {'form': form})


def excluir_hospital(request, hospital_id):
    """
    Exclui um hospital.
    """
    hospital = get_object_or_404(Hospital, id=hospital_id)
    hospital.delete()
    return redirect('listar_hospitais')

# ===========================
# 🔹 5️⃣ Vínculo de STEC ao Hospital
# ===========================
def vincular_hospital(request, id):
    """
    Realiza o vínculo de um usuário STEC a um Hospital.
    """
    hospital = get_object_or_404(Hospital, id=id)

    if request.method == 'POST':
        form = VinculoHospitalForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']

            # Verifica se já existe um Dashboard para esse usuário
            dashboard, created = Dashboard.objects.get_or_create(usuario=usuario)
            dashboard.hospital = hospital
            dashboard.role = 'STEC'
            dashboard.save()
            return redirect('listar_hospitais')
    else:
        form = VinculoHospitalForm(initial={'hospital': hospital})

    context = {
        'form': form,
        'hospital': hospital
    }
    return render(request, 'users/vincular_hospital.html', context)