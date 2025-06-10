from django.shortcuts import render, redirect
from django.contrib import messages
from users.models import PerfilUsuario
from gestaodeatas.models import AtaRegistroPreco
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

# Redireciona dashboard conforme papel do usuário
def redirecionar_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        perfil = PerfilUsuario.objects.get(usuario=request.user)
        if perfil.role == 'STEC':
            return redirect('dashboard_stec')
        elif perfil.role == 'SEC':
            return redirect('dashboard_sec')
        elif perfil.role == 'CEO':
            return redirect('dashboard_ceo')
    except PerfilUsuario.DoesNotExist:
        messages.error(request, "Seu usuário não está vinculado a um perfil de acesso.")
        return redirect('login')

# Dashboards dos perfis
def dashboard_stec(request):
    try:
        perfil = PerfilUsuario.objects.get(usuario=request.user)
        atas = AtaRegistroPreco.objects.filter(uasg=perfil.hospital.uasg)
    except PerfilUsuario.DoesNotExist:
        atas = []
        perfil = None
    return render(request, 'users/dashboard_stec.html', {'atas': atas, 'uasg': perfil.hospital.uasg if perfil else 'UASG indefinida'})

def dashboard_sec(request):
    atas = AtaRegistroPreco.objects.all()
    return render(request, 'users/dashboard_sec.html', {'atas': atas})

def dashboard_ceo(request):
    search = request.GET.get('search')
    hospital = request.GET.get('hospital')
    atas = AtaRegistroPreco.objects.filter(status='Homologada')
    if search:
        atas = atas.filter(numero_ata__icontains=search)
    if hospital:
        atas = atas.filter(hospital__icontains=hospital)
    return render(request, 'users/dashboard_ceo.html', {'atas': atas})

# Gera PDF com atas homologadas
def gerar_pdf_ceo(request):
    search = request.GET.get('search')
    hospital = request.GET.get('hospital')
    atas = AtaRegistroPreco.objects.filter(status='Homologada')
    if search:
        atas = atas.filter(numero_ata__icontains=search)
    if hospital:
        atas = atas.filter(hospital__icontains=hospital)
    html = render_to_string('users/relatorio_ceo.html', {'atas': atas})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio_atas.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    return response

# Sidebar views
def lista_atas(request):
    atas = AtaRegistroPreco.objects.all()
    return render(request, 'gestaodeatas/lista_atas.html', {'atas': atas})

def monitoramento_pncp(request):
    search = request.GET.get('search')
    uasg = request.GET.get('uasg')
    atas = AtaRegistroPreco.objects.all()
    if search:
        atas = atas.filter(numero_ata__icontains=search)
    if uasg:
        atas = atas.filter(uasg__icontains=uasg)
    return render(request, 'gestaodeatas/monitoramento_pncp.html', {'atas': atas})
