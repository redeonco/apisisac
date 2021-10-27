from django.db import models


class Patient(models.Model):
    id_paciente = models.CharField(primary_key=True, db_column='Pat_ID1', max_length=250)
    firstname = models.CharField(db_column='First_Name', blank=True, null=True, max_length=250)
    lastname = models.CharField(db_column='Last_Name', blank=True, null=True, max_length=250)
    cpf = models.CharField(db_column='SS_Number', blank=True, null=True, max_length=11)
    datanasc = models.DateTimeField(db_column='Birth_DtTm', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Patient'
    
    def __str__(self):
        return self.firstname   


class Schedule(models.Model):
    id_agenda = models.IntegerField(primary_key=True, db_column='Sch_Id')
    dataagenda = models.DateTimeField(db_column='App_DtTm', blank=True, null=True)
    id_paciente = models.ForeignKey(Patient, db_column='Pat_ID1', blank=True, null=True, max_length=250, on_delete=models.PROTECT)
    status = models.CharField(db_column='SchStatus_Hist_SD', blank=True, null=True, max_length=250)
    suppressed = models.CharField(db_column='Suppressed', blank=True, null=True, max_length=2)
    activity = models.CharField(db_column='Activity', blank=True, null=True, max_length=10)
    version = models.IntegerField(db_column='Version')
    edit_dt = models.DateTimeField(db_column='Edit_DtTm')
    create_dt = models.DateTimeField(db_column='Create_DtTm')

    class Meta:
        managed = False
        db_table = 'Schedule'
    
    def __str__(self):
        return str(self.id_agenda)


class PatCPlan(models.Model):
    pcp_id = models.IntegerField(primary_key=True, db_column='PCP_ID')
    id_paciente = models.ForeignKey(Patient, db_column='Pat_ID1', on_delete=models.PROTECT)
    intencao = models.CharField(db_column='Tx_Intent', max_length=20)

    class Meta:
        managed = False
        db_table = 'PatCPlan'

    def __str__(self):
        return str(self.intencao)


class Fase(models.Model):
    idfase = models.IntegerField(primary_key=True, db_column='SIT_ID')
    numerofase = models.IntegerField(db_column='DisplaySequence')
    id_paciente = models.ForeignKey(Patient, db_column='Pat_ID1', on_delete=models.PROTECT)
    locanatomica = models.CharField(db_column='Site_Name', max_length=20)
    modalidade = models.CharField(db_column='Modality', max_length=10)
    tecnica = models.CharField(db_column='Technique', max_length=20)
    dosediaria = models.IntegerField(db_column='Dose_Tx')
    dosetotal = models.IntegerField(db_column='Dose_Ttl')
    qtdsessoes = models.IntegerField(db_column='Fractions')
    create_dt = models.DateTimeField(db_column='Create_DtTm')
    edit_dt = models.DateTimeField(db_column='Edit_DtTm')
    sanct_dt = models.DateTimeField(db_column='Sanct_DtTm')
    version = models.IntegerField(db_column='Version')
    reference_sit_set_id = models.ForeignKey('self' ,db_column='Reference_SIT_Set_ID', on_delete=models.CASCADE)
    reference_fraction = models.IntegerField(db_column='Reference_Fraction')
    pcp_id = models.ForeignKey(PatCPlan, db_column='PCP_ID', on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'Site'

    def __str__(self):
        return str(self.idfase)

    def has_related_object(self):
        return hasattr(self, 'reference_sit_set_id')


class TxField(models.Model):
    id_campo = models.IntegerField(primary_key=True, db_column='FLD_ID')
    id_paciente = models.ForeignKey(Patient, db_column='Pat_ID1', on_delete=models.PROTECT)
    id_fase = models.ForeignKey(Fase, db_column='SIT_Set_ID', on_delete=models.PROTECT)
    nome_campo = models.CharField(db_column='Field_Name', max_length=20)
    numero_campo = models.IntegerField(db_column='DisplaySequence')
    dose_campo = models.IntegerField(db_column='Cgray')
    unidade_monitora = models.IntegerField(db_column='Meterset')
    create_dt = models.DateTimeField(db_column='Create_DtTm')
    edit_dt = models.DateTimeField(db_column='Edit_DtTm')
    sanct_dt = models.DateTimeField(db_column='Sanct_DtTm')
    version = models.IntegerField(db_column='Version')

    class Meta: 
        managed = False
        db_table = 'TxField'

    def __str__(self):
        return str(self.id_campo)


class TxFieldPoint(models.Model):
    tfp_id = models.IntegerField(primary_key=True, db_column='TFP_ID')
    id_campo = models.ForeignKey(TxField, db_column='FLD_ID', on_delete=models.PROTECT)
    energia = models.IntegerField(db_column='Energy')
    energia_unidade = models.IntegerField(db_column='Energy_Unit_Enum')
    gantry = models.IntegerField(db_column='Gantry_Ang')
    colimador = models.IntegerField(db_column='Coll_Ang')

    class Meta:
        managed = False
        db_table = 'TxFieldPoint'
    
    def __str__(self):
        return str(self.tfp_id)


class Dose_Hst(models.Model):
    dhs_id = models.IntegerField(primary_key=True, db_column='DHS_ID')
    id_paciente = models.ForeignKey(Patient, db_column='Pat_ID1', on_delete=models.PROTECT)
    datahora = models.DateTimeField(db_column='Create_DtTm')
    id_campo = models.ForeignKey(TxField, db_column='FLD_ID', on_delete=models.PROTECT)
    id_fase = models.ForeignKey(Fase, db_column='SIT_ID', on_delete=models.PROTECT)
    energia = models.IntegerField(db_column='Energy')
    dose_campo = models.IntegerField(db_column='Dose_Addtl_Projected')
    unidade_monitora = models.IntegerField(db_column='Meterset')

    class Meta:
        managed = False
        db_table = 'Dose_Hst'
    
    def __str__(self):
        return str(self.id_campo)
