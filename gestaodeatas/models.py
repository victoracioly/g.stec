from django.db import models

# Tipos possíveis para o status
STATUS_CHOICES = [
    ('Homologada', 'Homologada'),
    ('Cancelada', 'Cancelada'),
    ('Pendente', 'Pendente')
]

class AtaRegistroPreco(models.Model):
    numero_ata = models.CharField("Número da Ata", max_length=50, unique=True)
    edital = models.CharField("Edital", max_length=100, blank=True, null=True)
    uasg = models.CharField("UASG", max_length=20)
    hospital = models.CharField("Hospital", max_length=255)
    numero_sei = models.CharField("Número SEI", max_length=50, blank=True, null=True)
    vigencia_inicio = models.DateField("Vigência Inicial", blank=True, null=True)
    vigencia_fim = models.DateField("Vigência Final", blank=True, null=True)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='Pendente')

    # Novos campos identificados
    data_assinatura = models.DateField("Data de Assinatura", blank=True, null=True)
    data_publicacao_pncp = models.DateField("Data de Publicação PNCP", blank=True, null=True)
    data_inclusao = models.DateField("Data de Inclusão", blank=True, null=True)
    data_atualizacao = models.DateField("Data de Atualização", blank=True, null=True)
    objeto_contratacao = models.TextField("Objeto da Contratação", blank=True, null=True)
    nome_orgao = models.CharField("Nome do Órgão", max_length=255, blank=True, null=True)
    valor_total = models.DecimalField("Valor Total (R$)", max_digits=20, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Ata {self.numero_ata} - {self.hospital}"


class ItemDaAta(models.Model):
    ata = models.ForeignKey(AtaRegistroPreco, on_delete=models.CASCADE, related_name="itens")
    nome_item = models.CharField("Nome do Item", max_length=255)
    marca = models.CharField("Marca", max_length=100)
    modelo = models.CharField("Modelo", max_length=100)
    garantia_meses = models.PositiveIntegerField("Garantia (meses)")
    valor = models.DecimalField("Valor (R$)", max_digits=15, decimal_places=2)
    empresa = models.CharField("Empresa", max_length=255)
    item_no_srp = models.CharField("Item no SRP", max_length=50)
    tipo_item = models.CharField("Tipo de Item", max_length=10, choices=[('bem', 'Bem'), ('servico', 'Serviço')], default='bem')
    descricao_corrigida = models.TextField("Descrição Corrigida", blank=True, null=True)
    corrigido_por = models.CharField("Corrigido por", max_length=255, blank=True, null=True)
    catmat_sugerido = models.CharField("CATMAT Sugerido", max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nome_item} - {self.empresa}"
