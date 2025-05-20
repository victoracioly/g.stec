# forms.py
from django import forms
from django.forms import modelformset_factory
from .models import AtaRegistroPreco, ItemDaAta

class AtaRegistroPrecoForm(forms.ModelForm):
    class Meta:
        model = AtaRegistroPreco
        fields = '__all__'

class ItemDaAtaForm(forms.ModelForm):
    class Meta:
        model = ItemDaAta
        fields = [
            'nome_item', 'marca', 'modelo', 'garantia_meses',
            'valor', 'empresa', 'item_no_srp', 'tipo_item',
            'descricao_corrigida', 'corrigido_por', 'catmat_sugerido',
        ]
        widgets = {
            'descricao_corrigida': forms.HiddenInput(),
            'corrigido_por': forms.HiddenInput(),
            'catmat_sugerido': forms.HiddenInput(),
        }

ItemFormSet = modelformset_factory(
    ItemDaAta,
    form=ItemDaAtaForm,
    extra=1,
    can_delete=True
)
