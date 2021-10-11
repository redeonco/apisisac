from django.db import models


class Patient(models.Model):
    id_paciente = models.CharField(primary_key=True, db_column='Pat_ID1', max_length=250)
    firstname = models.CharField(db_column='First_Name', blank=True, null=True, max_length=250)
    lastname = models.CharField(db_column='Last_Name', blank=True, null=True, max_length=250)
    datanasc = models.DateTimeField(db_column='Birth_DtTm', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Patient'
    
    def __str__(self):
        return self.firstname   


class Schedule(models.Model):
    id_agenda = models.IntegerField(primary_key=True, db_column='Sch_Id', max_length=250)
    dataagenda = models.DateTimeField(db_column='App_DtTm', blank=True, null=True)
    id_paciente = models.ForeignKey(Patient, db_column='Pat_ID1', blank=True, null=True, max_length=250, on_delete=models.PROTECT)
    status = models.CharField(db_column='SchStatus_Hist_SD', blank=True, null=True, max_length=250)

    class Meta:
        managed = False
        db_table = 'Schedule'
    
    def __str__(self):
        return str(self.id_agenda)
