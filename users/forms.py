# users/forms.py
from django import forms
from .models import Hospital, Dashboard
from django.contrib.auth.models import User


class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['nome', 'uasg', 'cnpj', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Hospital'}),
            'uasg': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UASG'}),
            'cnpj': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CNPJ'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Endereço', 'rows': 3}),
        }
        labels = {
            'nome': 'Nome do Hospital',
            'uasg': 'UASG',
            'cnpj': 'CNPJ',
            'endereco': 'Endereço Completo',
        }

    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')
        if len(cnpj) != 18:  # Verifica se está no formato '00.000.000/0000-00'
            raise forms.ValidationError("O CNPJ deve estar no formato 12.345.678/0000-00")
        return cnpj


# ===========================
# Formulário para Vínculo do STEC ao Hospital
# ===========================
class VinculoHospitalForm(forms.ModelForm):
    usuario = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='STEC'),
        label="Usuário (STEC)",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Dashboard
        fields = ['usuario', 'hospital']
        widgets = {
            'hospital': forms.HiddenInput()
        }
