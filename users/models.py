from django.contrib.auth.models import Group, User
from django.db import models

PERMISSOES = {
    'STEC': 'Permissão de acesso restrito à UASG',
    'SEC': 'Acesso total aos dados das unidades',
    'CEO': 'Visualização de relatórios gerais'
}

CARGO_CHOICES = [
    ('ENGENHEIRO', 'Engenheiro Clínico'),
    ('ASSISTENTE', 'Assistente Administrativo'),
    ('ANALISTA', 'Analista Administrativo'),
    ('DIRETOR', 'Diretor'),
]

ROLE_CHOICES = [
    ('STEC', 'STEC'),
    ('SEC', 'SEC'),
    ('CEO', 'CEO'),
]

class Hospital(models.Model):
    nome = models.CharField(max_length=255)
    uasg = models.CharField(max_length=10, unique=True)
    cnpj = models.CharField(max_length=18, unique=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=2, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.uasg}"

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=255)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES)

    def __str__(self):
        return f"{self.nome_completo} - {self.get_role_display()} - {self.get_cargo_display()}"

    def get_perfil_resumo(self):
        if self.role == 'STEC' and self.hospital:
            return f"Acesso STEC - {self.hospital.nome}"
        elif self.role == 'SEC':
            return "Acesso SEC - Visualização Global"
        elif self.role == 'CEO':
            return "Acesso CEO - Relatórios Institucionais"
        return "Acesso não identificado"
