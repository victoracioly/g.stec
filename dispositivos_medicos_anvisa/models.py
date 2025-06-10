from django.db import models

class DispositivoMedicoAnvisa(models.Model):
    numero_registro_cadastro = models.CharField(max_length=50)
    numero_processo = models.CharField(max_length=50, blank=True, null=True)
    nome_tecnico = models.CharField(max_length=255, blank=True, null=True)
    classe_risco = models.CharField(max_length=50, blank=True, null=True)
    nome_comercial = models.CharField(max_length=255, blank=True, null=True)
    cnpj_detentor_registro = models.CharField(max_length=20, blank=True, null=True)
    detentor_registro = models.CharField(max_length=255, blank=True, null=True)
    nome_fabricante = models.CharField(max_length=255, blank=True, null=True)
    nome_pais_fabricante = models.CharField(max_length=100, blank=True, null=True)
    data_publicacao_registro = models.DateField(blank=True, null=True)
    validade_registro = models.DateField(blank=True, null=True)
    data_atualizacao = models.DateField(blank=True, null=True)
    #Como alguns campos são datas e outros podem vir vazios no Excel, 
    #é bom usar blank=True, null=True para evitar erros durante o parsing.

    def __str__(self):
        return f"{self.nome_comercial} ({self.numero_registro_cadastro})"
