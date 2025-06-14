from django.shortcuts import render
from dispositivos_medicos_anvisa.models import DispositivoMedicoAnvisa
from datetime import date
from django.db.models import Q, Count, Max, Case, When, Value, IntegerField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

def build_q_object(field_name, terms):
    q = Q()
    for term in terms:
        t = term.strip()
        if t:
            q |= Q(**{f"{field_name}__icontains": t})
    return q

def lista_dispositivos(request):
    qs = DispositivoMedicoAnvisa.objects.all()

    nome_comercial  = request.GET.get('nome_comercial', '').strip()
    numero_registro = request.GET.get('numero_registro', '').strip()
    fabricante      = request.GET.get('fabricante', '').strip()
    pais_fabricante = request.GET.get('pais_fabricante', '').strip()
    classe_risco    = request.GET.get('classe_risco', '').strip()

    if nome_comercial:
        qs = qs.filter(build_q_object('nome_comercial', nome_comercial.split(',')))
    if numero_registro:
        qs = qs.filter(build_q_object('numero_registro_cadastro', numero_registro.split(',')))
    if fabricante:
        qs = qs.filter(build_q_object('nome_fabricante', fabricante.split(',')))
    if pais_fabricante:
        qs = qs.filter(build_q_object('nome_pais_fabricante', pais_fabricante.split(',')))
    if classe_risco:
        qs = qs.filter(build_q_object('classe_risco', classe_risco.split(',')))

    total_dispositivos = qs.count()

    top_paises = (
        qs.values('nome_pais_fabricante')
          .exclude(nome_pais_fabricante__exact='')
          .annotate(total=Count('id'))
          .order_by('-total')[:3]
    )
    top_fabricantes = (
        qs.values('nome_fabricante')
          .exclude(nome_fabricante__exact='')
          .annotate(total=Count('id'))
          .order_by('-total')[:3]
    )

    ultima = DispositivoMedicoAnvisa.objects.aggregate(ultima=Max('data_atualizacao'))['ultima']
    ultima_atualizacao = ultima.strftime('%d/%m/%Y') if ultima else '—'

    qs = qs.annotate(
        is_date=Case(
            When(validade_registro__regex=r'^\d{4}-\d{2}-\d{2}$', then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )
    ).order_by('-is_date', 'validade_registro')

    paginator = Paginator(qs, 1000)
    try:
        dispositivos = paginator.page(request.GET.get('page'))
    except (PageNotAnInteger, EmptyPage):
        dispositivos = paginator.page(1)

    for d in dispositivos:
        vr = d.validade_registro or ''
        d.validade_display = vr or 'VIGENTE'

    return render(request,
                  'dispositivos_medicos_anvisa/lista_dispositivos_medicos_anvisa.html',
                  {
                      'dispositivos': dispositivos,
                      'total_dispositivos': total_dispositivos,
                      'top_paises': top_paises,
                      'top_fabricantes': top_fabricantes,
                      'ultima_atualizacao': ultima_atualizacao,
                      'filtros': [],
                  })

def exportar_dispositivos_pdf(request):
    qs = DispositivoMedicoAnvisa.objects.all()
    filtros = []

    campos = [
        ('nome_comercial', 'Nome Comercial'),
        ('numero_registro_cadastro', 'Nº Registro'),
        ('nome_fabricante', 'Fabricante'),
        ('nome_pais_fabricante', 'País do Fabricante'),
        ('classe_risco', 'Classe de Risco'),
    ]
    param_map = {
        'nome_comercial': 'nome_comercial',
        'numero_registro_cadastro': 'numero_registro',
        'nome_fabricante': 'fabricante',
        'nome_pais_fabricante': 'pais_fabricante',
        'classe_risco': 'classe_risco',
    }

    for field, label in campos:
        param = param_map.get(field, field)
        valor = request.GET.get(param, '').strip()
        if valor:
            qs = qs.filter(build_q_object(field, valor.split(',')))
            filtros.append(f"{label}: {', '.join(valor.split(','))}")

    qs = qs.annotate(
        is_date=Case(
            When(validade_registro__regex=r'^\d{4}-\d{2}-\d{2}$', then=Value(1)),
            default=Value(0),
            output_field=IntegerField(),
        )
    ).order_by('-is_date', 'validade_registro')

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=20, leftMargin=20,
                            topMargin=20, bottomMargin=20)
    styles = getSampleStyleSheet()
    elements = [Paragraph("Relatório de Dispositivos Médicos", styles['Title']), Spacer(1, 12)]

    if filtros:
        elements.append(Paragraph("Filtros Aplicados:", styles['Heading2']))
        for f in filtros:
            elements.append(Paragraph(f, styles['Normal']))
        elements.append(Spacer(1, 12))

    data = [['#', 'Registro', 'Nome Comercial', 'Fabricante',
             'País', 'Classe', 'Publicação', 'Validade']]
    for idx, d in enumerate(qs, start=1):
        vr = d.validade_registro or ''
        validade = vr or 'VIGENTE'
        data.append([
            str(idx),
            d.numero_registro_cadastro,
            Paragraph(d.nome_comercial or '', styles['Normal']),
            Paragraph(d.nome_fabricante or '', styles['Normal']),
            Paragraph(d.nome_pais_fabricante or '', styles['Normal']),
            d.classe_risco or '',
            d.data_publicacao_registro.strftime('%d/%m/%Y') if d.data_publicacao_registro else '',
            validade,
        ])

    table = Table(data, repeatRows=1, colWidths=[20, 60, 130, 100, 70, 30, 50, 50])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR',  (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN',      (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING',(0, 0),(-1, 0),6),
        ('GRID',       (0, 0),(-1, -1),0.25,colors.black),
        ('VALIGN',     (0, 0),(-1, -1),'TOP'),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(
        "Fonte: https://www.gov.br/anvisa/pt-br/assuntos/produtosparasaude/" +
        "lista-de-dispositivos-medicos-regularizados",
        styles['Normal']
    ))

    doc.build(elements)
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
