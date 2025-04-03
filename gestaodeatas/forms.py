from django import forms
from django.forms import inlineformset_factory
from .models import AtaRegistroPreco, ItemDaAta

class AtaRegistroPrecoForm(forms.ModelForm):
    vigencia_inicio = forms.DateField(input_formats=['%d/%m/%Y'])
    vigencia_fim = forms.DateField(input_formats=['%d/%m/%Y'])

    class Meta:
        model = AtaRegistroPreco
        fields = '__all__'

class ItemDaAtaForm(forms.ModelForm):
    class Meta:
        model = ItemDaAta
        exclude = ['ata', 'id']  # oculta os campos no HTML

# Criação do formset para múltiplos itens da ata
ItemFormSet = inlineformset_factory(
    AtaRegistroPreco,
    ItemDaAta,
    form=ItemDaAtaForm,
    extra=1,
    can_delete=True
)