from django.shortcuts import render, redirect, get_object_or_404
from .models import AtaRegistroPreco
from .forms import AtaRegistroPrecoForm, ItemFormSet

# Página inicial: lista todas as atas
def pagina_inicial(request):
    atas = AtaRegistroPreco.objects.all()
    return render(request, 'gestaodeatas/lista_atas.html', {'atas': atas})

# Criação de nova ata
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
            return redirect('lista_atas')
    else:
        form = AtaRegistroPrecoForm()
        formset = ItemFormSet(queryset=ItemFormSet.model.objects.none())
    
    return render(request, 'gestaodeatas/nova_ata.html', {
        'form': form,
        'formset': formset,
    })

# Detalhes de uma ata específica
def detalhes_ata(request, id):
    ata = get_object_or_404(AtaRegistroPreco, id=id)
    return render(request, 'gestaodeatas/detalhes_ata.html', {'ata': ata})
