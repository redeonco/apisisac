from django.db import models


class ControlPacientes(models.Model):
    codpac_sisac = models.CharField(max_length=10, blank=True, null=True)
    id_paciente_mosaiq = models.CharField(max_length=10)
    cpf = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return str(self.codpac_sisac)


class Usuarios(models.Model):
    username = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user_id = models.IntegerField()
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.username


class EmailDestinatario(models.Model):
    email = models.EmailField(max_length=250)

    def __str__(self):
        return self.email
