from django.db import models


class ControlPacientes(models.Model):
    codpac_sisac = models.CharField(max_length=10, blank=True, null=True)
    id_paciente_mosaiq = models.CharField(max_length=10)
    cpf = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return str(self.codpac_sisac)
