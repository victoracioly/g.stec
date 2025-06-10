from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from users.models import Hospital, PerfilUsuario

class UserCreationExtendedForm(forms.ModelForm):
    nome_completo = forms.CharField(
        max_length=255,
        label="Nome completo",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo igual ao Teams'})
    )
    telefone = forms.CharField(
        required=False,
        label="Telefone",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'})
    )
    hospital = forms.ModelChoiceField(
        queryset=Hospital.objects.all(),
        required=False,
        label="Hospital",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    cargo = forms.ChoiceField(
        choices=PerfilUsuario._meta.get_field('cargo').choices,
        label="Cargo",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    role = forms.ChoiceField(
        choices=PerfilUsuario._meta.get_field('role').choices,
        label="Permissão",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['email']  # Só o email no model User

    def clean_nome_completo(self):
        nome = self.cleaned_data.get('nome_completo', '').strip()
        partes = nome.split()
        if len(partes) < 2:
            raise ValidationError("Por favor, informe o nome completo (nome e sobrenome), como aparece no Teams.")
        return nome

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este e-mail já está cadastrado.")
        return email

    def save(self, commit=True):
        # Cria o usuário no model User
        user = super().save(commit=False)
        # Define username automaticamente, ex: user_1, user_2, etc.
        user.username = f"user_{User.objects.count() + 1}"
        # Define senha padrão (deve mudar depois)
        user.set_password("123456")

        if commit:
            user.save()
            # Cria o PerfilUsuario associado
            PerfilUsuario.objects.create(
                usuario=user,
                nome_completo=self.cleaned_data['nome_completo'],
                telefone=self.cleaned_data.get('telefone'),
                hospital=self.cleaned_data.get('hospital'),
                cargo=self.cleaned_data['cargo'],
                role=self.cleaned_data['role'],
            )
        return user


class HospitalForm(forms.ModelForm):
    class Meta:
        model = Hospital
        fields = ['nome', 'uasg', 'cidade', 'estado']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do hospital'}),
            'uasg': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UASG'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Cidade'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado'}),
        }


class VinculoHospitalForm(forms.Form):
    usuario = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    role = forms.ChoiceField(
        choices=PerfilUsuario._meta.get_field('role').choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    cargo = forms.ChoiceField(
        choices=PerfilUsuario._meta.get_field('cargo').choices,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
