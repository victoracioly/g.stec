from django.shortcuts import render
from dispositivos_medicos_anvisa.models import DispositivoMedicoAnvisa
from datetime import date
from django.db.models import Count, Max, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# Utilitário de múltiplos termos
def build_q_object(field_name, terms):
    q_object = Q()
    for term in terms:
        q_object |= Q(**{f"{field_name}__icontains": term.strip()})
    return q_object

def lista_dispositivos(request):
    dispositivos = DispositivoMedicoAnvisa.objects.all()

    # Campos com múltiplos termos separados por vírgula
    nome_comercial = request.GET.get('nome_comercial')
    numero_registro = request.GET.get('numero_registro')
    fabricante = request.GET.get('fabricante')
    pais_fabricante = request.GET.get('pais_fabricante')
    classe_risco = request.GET.get('classe_risco')
    vigentes = request.GET.get('vigentes')

    if nome_comercial:
        termos = nome_comercial.split(',')
        dispositivos = dispositivos.filter(build_q_object('nome_comercial', termos))
    if numero_registro:
        termos = numero_registro.split(',')
        dispositivos = dispositivos.filter(build_q_object('numero_registro_cadastro', termos))
    if fabricante:
        termos = fabricante.split(',')
        dispositivos = dispositivos.filter(build_q_object('nome_fabricante', termos))
    if pais_fabricante:
        termos = pais_fabricante.split(',')
        dispositivos = dispositivos.filter(build_q_object('nome_pais_fabricante', termos))
    if classe_risco:
        termos = classe_risco.split(',')
        dispositivos = dispositivos.filter(build_q_object('classe_risco', termos))
    if vigentes == '1':
        dispositivos = dispositivos.filter(
            Q(validade_registro__gte=date.today()) |
            Q(validade_registro__iexact="VIGENTE")
        )

    total_dispositivos = dispositivos.count()

    top_paises = dispositivos.values('nome_pais_fabricante')\
        .exclude(nome_pais_fabricante__isnull=True)\
        .exclude(nome_pais_fabricante='')\
        .annotate(total=Count('id'))\
        .order_by('-total')[:3]

    top_fabricantes = dispositivos.values('nome_fabricante')\
        .exclude(nome_fabricante__isnull=True)\
        .exclude(nome_fabricante='')\
        .annotate(total=Count('id'))\
        .order_by('-total')[:3]

    ultima_atualizacao = DispositivoMedicoAnvisa.objects.aggregate(
        ultima=Max('data_atualizacao'))['ultima']

    dispositivos = dispositivos.order_by('validade_registro')

    paginator = Paginator(dispositivos, 1000)
    page = request.GET.get('page')
    try:
        dispositivos_paginados = paginator.page(page)
    except PageNotAnInteger:
        dispositivos_paginados = paginator.page(1)
    except EmptyPage:
        dispositivos_paginados = paginator.page(paginator.num_pages)

    return render(request, 'dispositivos_medicos_anvisa/lista_dispositivos_medicos_anvisa.html', {
        'dispositivos': dispositivos_paginados,
        'top_paises': top_paises,
        'top_fabricantes': top_fabricantes,
        'total_dispositivos': total_dispositivos,
        'ultima_atualizacao': ultima_atualizacao
    })

def exportar_dispositivos_pdf(request):
    dispositivos = DispositivoMedicoAnvisa.objects.all()

    filtros = []
    campos = [
        ('nome_comercial', 'Nome Comercial'),
        ('numero_registro', 'Nº Registro'),
        ('fabricante', 'Fabricante'),
        ('pais_fabricante', 'País do Fabricante'),
        ('classe_risco', 'Classe de Risco'),
    ]

    for param, label in campos:
        valor = request.GET.get(param)
        if valor:
            termos = valor.split(',')
            dispositivos = dispositivos.filter(build_q_object(param if param != 'fabricante' else 'nome_fabricante', termos))
            filtros.append(f"{label}: {', '.join(termos)}")

    if request.GET.get('vigentes') == '1':
        dispositivos = dispositivos.filter(
            Q(validade_registro__gte=date.today()) |
            Q(validade_registro__iexact="VIGENTE")
        )
        filtros.append("Somente Vigentes")

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Relatório de Dispositivos Médicos", styles['Title']))
    elements.append(Spacer(1, 12))

    if filtros:
        elements.append(Paragraph("Filtros Aplicados:", styles['Heading2']))
        for filtro in filtros:
            elements.append(Paragraph(filtro, styles['Normal']))
        elements.append(Spacer(1, 12))

    data = [['#', 'Registro', 'Nome Comercial', 'Fabricante', 'País', 'Classe', 'Publicação', 'Validade']]
    for idx, d in enumerate(dispositivos, start=1):
        data.append([
            str(idx),
            d.numero_registro_cadastro,
            Paragraph(d.nome_comercial or '', styles['Normal']),
            Paragraph(d.nome_fabricante or '', styles['Normal']),
            Paragraph(d.nome_pais_fabricante or '', styles['Normal']),
            d.classe_risco or '',
            d.data_publicacao_registro.strftime('%d/%m/%Y') if d.data_publicacao_registro else '',
            d.validade_registro.strftime('%d/%m/%Y') if d.validade_registro else ''
        ])

    table = Table(data, repeatRows=1, colWidths=[20, 60, 130, 100, 70, 30, 50, 50])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    elements.append(table)

    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        "Fonte: https://www.gov.br/anvisa/pt-br/assuntos/produtosparasaude/lista-de-dispositivos-medicos-regularizados",
        styles['Normal']))

    doc.build(elements)
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
