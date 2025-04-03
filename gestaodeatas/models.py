from django.db import models

class AtaRegistroPreco(models.Model):
    numero_ata = models.CharField(max_length=50, unique=True)
    edital = models.CharField(max_length=100)
    uasg = models.CharField(max_length=20)
    hospital = models.CharField(max_length=255)
    numero_sei = models.CharField(max_length=50)
    vigencia_inicio = models.DateField()
    vigencia_fim = models.DateField()

    def __str__(self):
        return f"Ata {self.numero_ata} - {self.hospital}"


class ItemDaAta(models.Model):
    ata = models.ForeignKey(AtaRegistroPreco, on_delete=models.CASCADE, related_name="itens")
    nome_item = models.CharField(max_length=255)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    garantia_meses = models.PositiveIntegerField()
    valor = models.DecimalField(max_digits=15, decimal_places=2)
    empresa = models.CharField(max_length=255)
    item_no_srp = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome_item} - {self.empresa}"

