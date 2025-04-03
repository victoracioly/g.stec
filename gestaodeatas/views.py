from django.shortcuts import render, get_object_or_404, redirect
from .models import AtaRegistroPreco, ItemDaAta
from .forms import AtaRegistroPrecoForm, ItemDaAtaForm, ItemFormSet
from django.db.models import Q
from datetime import date

def lista_atas(request):
    query = request.GET.get('q', '')
    apenas_vigentes = request.GET.get('vigentes') == 'on'
    hoje = date.today()

    atas = AtaRegistroPreco.objects.all()

    if query:
        atas = atas.filter(
            Q(numero_ata__icontains=query) |
            Q(hospital__icontains=query) |
            Q(uasg__icontains=query) |
            Q(numero_sei__icontains=query)
        )

    if apenas_vigentes:
        atas = atas.filter(vigencia_fim__gte=hoje)

    return render(request, 'gestaodeatas/lista_atas.html', {
        'atas': atas,
        'query': query,
        'apenas_vigentes': apenas_vigentes
    })

def detalhes_ata(request, ata_id):
    ata = get_object_or_404(AtaRegistroPreco, id=ata_id)
    return render(request, 'gestaodeatas/detalhes_ata.html', {'ata': ata})

def nova_ata(request):
    if request.method == 'POST':
        form = AtaRegistroPrecoForm(request.POST)
        formset = ItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            ata = form.save()
            itens = formset.save(commit=False)
            for item in itens:
                item.ata = ata
                item.save()
            return redirect('detalhes_ata', ata_id=ata.id)
    else:
        form = AtaRegistroPrecoForm()
        formset = ItemFormSet()

    return render(request, 'gestaodeatas/nova_ata.html', {
        'form': form,
        'formset': formset
    })




