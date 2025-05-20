from django.contrib.auth.models import Group, Permission, User
from django.db import models

# ====== Modelagem de Perfis ======
# Grupos de usuários
GROUPS = {
    'STEC': 'Setor de Engenharia Clínica',
    'SEC': 'Serviço de Engenharia Clínica',
    'CEO': 'CEO da EBSERH'
}

# Função para criar os grupos e permissões
def criar_grupos():
    """
    Função para criar os grupos de usuários (perfis) no banco de dados.
    Se o grupo já existir, ele apenas ignora e segue.
    """
    for group_name, description in GROUPS.items():
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            print(f"Grupo {description} criado com sucesso.")


# ====== Modelagem de Hospital ======
class Hospital(models.Model):
    nome = models.CharField(max_length=255)
    uasg = models.CharField(max_length=10, unique=True)
    cnpj = models.CharField(max_length=18, unique=True)  # Inclui máscara de CNPJ
    endereco = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nome} - {self.uasg}"


# ====== Modelagem dos Dashboards ======
class Dashboard(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=20, choices=[('STEC', 'STEC'), ('SEC', 'SEC'), ('CEO', 'CEO')])
    
    def __str__(self):
        return f"{self.usuario.username} - {self.role}"

    def get_dashboard_data(self):
        if self.role == 'STEC' and self.hospital:
            return f"Dashboard do STEC para o Hospital: {self.hospital.nome}"
        elif self.role == 'SEC':
            return "Dashboard do SEC - Visualização Global"
        elif self.role == 'CEO':
            return "Dashboard Resumido para CEO"
        else:
            return "Perfil não identificado"
