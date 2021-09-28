from django.db import models


class Cadpaciente(models.Model):
    codpaciente = models.CharField(db_column='CODPACIENTE', primary_key=True, max_length=10)  # Field name made lowercase.
    paciente = models.CharField(db_column='PACIENTE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sexo = models.CharField(db_column='SEXO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    datanasc = models.DateTimeField(db_column='DATANASC', blank=True, null=True)  # Field name made lowercase.
    idade = models.CharField(db_column='IDADE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rg = models.CharField(db_column='RG', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cpf = models.CharField(db_column='CPF', max_length=15, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CADPACIENTE'
        unique_together = (('codpaciente', 'cpf'),)

    def __str__(self):
        return self.paciente


class ApiEntrada(models.Model):
    codpaciente = models.CharField(db_column='CodPaciente', max_length=10, blank=True, null=True)  # Field name made lowercase.
    paciente = models.CharField(db_column='Paciente', max_length=200, blank=True, null=True)  # Field name made lowercase.
    codmovimento = models.CharField(db_column='CodMovimento', primary_key=True, max_length=10)  # Field name made lowercase.
    matricula = models.CharField(db_column='Matricula', max_length=30, blank=True, null=True)  # Field name made lowercase.
    tipoatd = models.CharField(db_column='TipoAtd', max_length=25, blank=True, null=True)  # Field name made lowercase.
    situacao = models.CharField(db_column='Situacao', max_length=20, blank=True, null=True)  # Field name made lowercase.
    datahoraent = models.DateTimeField(db_column='DataHoraEnt', blank=True, null=True)  # Field name made lowercase.
    datahorasai = models.DateTimeField(db_column='DataHoraSai', blank=True, null=True)  # Field name made lowercase.
    codconvenio = models.CharField(db_column='CodConvenio', max_length=6, blank=True, null=True)  # Field name made lowercase.
    convenio = models.CharField(db_column='Convenio', max_length=100, blank=True, null=True)  # Field name made lowercase.
    plano = models.CharField(db_column='Plano', max_length=100, blank=True, null=True)  # Field name made lowercase.
    codmedico = models.CharField(db_column='CodMedico', max_length=6, blank=True, null=True)  # Field name made lowercase.
    medico = models.CharField(db_column='Medico', max_length=200, blank=True, null=True)  # Field name made lowercase.
    codamb = models.CharField(db_column='CodAmb', max_length=20, blank=True, null=True)  # Field name made lowercase.
    procedimento = models.CharField(db_column='Procedimento', max_length=500, blank=True, null=True)  # Field name made lowercase.
    hist = models.CharField(db_column='Hist', max_length=200, blank=True, null=True)  # Field name made lowercase.
    total = models.FloatField(db_column='Total', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'API_Entrada'

    def __str__(self):
        return self.codmovimento


class ApiConsulta(models.Model):
    codpaciente = models.CharField(db_column='CodPaciente', max_length=10, blank=True, null=True)  # Field name made lowercase.
    paciente = models.CharField(db_column='Paciente', max_length=200, blank=True, null=True)  # Field name made lowercase.
    # codmovimento = models.CharField(primary_key=True, db_column='CodMovimento', max_length=10)  # Field name made lowercase.
    codmovimento = models.ForeignKey(ApiEntrada, db_column='CodMovimento', max_length=10, on_delete=models.PROTECT)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    codconvenio = models.CharField(db_column='CodConvenio', max_length=6, blank=True, null=True)  # Field name made lowercase.
    convenio = models.CharField(db_column='Convenio', max_length=100, blank=True, null=True)  # Field name made lowercase.
    historico = models.TextField(db_column='Historico', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    data = models.DateTimeField(db_column='Data', blank=True, null=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=100, blank=True, null=True)  # Field name made lowercase.
    obs = models.CharField(db_column='Obs', max_length=100, blank=True, null=True)  # Field name made lowercase.
    numpresc = models.CharField(db_column='NumPresc', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codmedico = models.CharField(db_column='CodMedico', max_length=10, blank=True, null=True)  # Field name made lowercase.
    medico = models.CharField(db_column='Medico', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'API_Consulta'

    def __str__(self):
        return self.codmovimento


class ApiEnfevoluc(models.Model):
    ndoc = models.CharField(db_column='NDoc', max_length=11, blank=True, null=True)  # Field name made lowercase.
    codpaciente = models.CharField(primary_key=True, db_column='CodPaciente', max_length=11)  # Field name made lowercase.
    paciente = models.CharField(db_column='Paciente', max_length=200, blank=True, null=True)  # Field name made lowercase.
    acomod = models.CharField(db_column='Acomod', max_length=50, blank=True, null=True)  # Field name made lowercase.
    datahoraf = models.DateTimeField(db_column='DataHoraF', blank=True, null=True)  # Field name made lowercase.
    codmedico = models.CharField(db_column='CodMedico', max_length=11, blank=True, null=True)  # Field name made lowercase.
    enfermeiro = models.CharField(db_column='Enfermeiro', max_length=200, blank=True, null=True)  # Field name made lowercase.
    texto3 = models.TextField(db_column='Texto3', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = 'API_EnfEvoluC'

    def __str__(self):
        return self.codpaciente


class ApiEntradaradio(models.Model):
    identradaradio = models.CharField(primary_key=True, db_column='idEntradaRadio', max_length=10)  # Field name made lowercase.
    codmovimento = models.CharField(db_column='CodMovimento', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codpaciente = models.CharField(db_column='CodPaciente', max_length=10, blank=True, null=True)  # Field name made lowercase.
    paciente = models.CharField(db_column='Paciente', max_length=200, blank=True, null=True)  # Field name made lowercase.
    numpresc = models.CharField(db_column='NumPresc', max_length=10, blank=True, null=True)  # Field name made lowercase.
    idplanejfisico = models.CharField(db_column='idPlanejFisico', max_length=10, blank=True, null=True)  # Field name made lowercase.
    encerrado = models.CharField(db_column='Encerrado', max_length=10, blank=True, null=True)  # Field name made lowercase.
    observacao = models.CharField(db_column='Observacao', max_length=200, blank=True, null=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=20, blank=True, null=True)  # Field name made lowercase.
    datahora = models.DateTimeField(db_column='DataHora', blank=True, null=True)  # Field name made lowercase.
    nplanejamento = models.IntegerField(db_column='NPlanejamento', blank=True, null=True)  # Field name made lowercase.
    nomecampo = models.CharField(db_column='NomeCampo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    incidencia = models.CharField(db_column='Incidencia', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ncampo = models.IntegerField(db_column='NCampo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'API_EntradaRadio'

    def __str__(self):
        return self.codmovimento


class ApiPlanejfisicoc(models.Model):
    idplanejfisicoc = models.CharField(primary_key=True, db_column='idPlanejFisicoC', max_length=10)  # Field name made lowercase.
    codpaciente = models.CharField(db_column='CodPaciente', max_length=11, blank=True, null=True)  # Field name made lowercase.
    paciente = models.CharField(db_column='Paciente', max_length=200, blank=True, null=True)  # Field name made lowercase.
    numpresc = models.CharField(db_column='NumPresc', max_length=10, blank=True, null=True)  # Field name made lowercase.
    aparelho = models.CharField(db_column='Aparelho', max_length=50, blank=True, null=True)  # Field name made lowercase.
    energia = models.CharField(db_column='Energia', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dosetotal = models.CharField(db_column='DoseTotal', max_length=20, blank=True, null=True)  # Field name made lowercase.
    dosediaria = models.CharField(db_column='DoseDiaria', max_length=20, blank=True, null=True)  # Field name made lowercase.
    naplicacoes = models.IntegerField(db_column='NAplicacoes', blank=True, null=True)  # Field name made lowercase.
    dosemonitor = models.CharField(db_column='DoseMonitor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    locanatomica = models.CharField(db_column='LocAnatomica', max_length=50, blank=True, null=True)  # Field name made lowercase.
    incidencia = models.CharField(db_column='Incidencia', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ncampo = models.IntegerField(db_column='NCampo', blank=True, null=True)  # Field name made lowercase.
    portal = models.IntegerField(db_column='Portal', blank=True, null=True)  # Field name made lowercase.
    tpfeixe = models.CharField(db_column='TpFeixe', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fase = models.IntegerField(db_column='Fase', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'API_PlanejFisicoC'

    def __str__(self):
        return self.codmovimento


class ApiPrescreve(models.Model):
    codpaciente = models.CharField(db_column='CodPaciente', max_length=11, blank=True, null=True)  # Field name made lowercase.
    codpacref = models.CharField(db_column='CodPacRef', max_length=10, blank=True, null=True)  # Field name made lowercase.
    paciente = models.CharField(db_column='Paciente', max_length=200, blank=True, null=True)  # Field name made lowercase.
    codmedico = models.CharField(db_column='CodMedico', max_length=10, blank=True, null=True)  # Field name made lowercase.
    medico = models.CharField(db_column='Medico', max_length=200, blank=True, null=True)  # Field name made lowercase.
    data = models.DateTimeField(db_column='Data', blank=True, null=True)  # Field name made lowercase.
    numero = models.CharField(primary_key=True, db_column='Numero', max_length=10)  # Field name made lowercase.
    texto = models.TextField(db_column='Texto', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    obs = models.CharField(db_column='Obs', max_length=150, blank=True, null=True)  # Field name made lowercase.
    aplicado = models.CharField(db_column='Aplicado', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'API_Prescreve'

    def __str__(self):
        return self.codpaciente


class ApiPrescreveqt(models.Model):
    codpaciente = models.CharField(db_column='CodPaciente', max_length=11, blank=True, null=True)  # Field name made lowercase.
    codpacref = models.CharField(db_column='CodPacRef', max_length=10, blank=True, null=True)  # Field name made lowercase.
    paciente = models.CharField(db_column='Paciente', max_length=200, blank=True, null=True)  # Field name made lowercase.
    codmedico = models.CharField(db_column='CodMedico', max_length=10, blank=True, null=True)  # Field name made lowercase.
    medico = models.CharField(db_column='Medico', max_length=200, blank=True, null=True)  # Field name made lowercase.
    data = models.DateTimeField(db_column='Data', blank=True, null=True)  # Field name made lowercase.
    numero = models.CharField(primary_key=True, db_column='Numero', max_length=10)  # Field name made lowercase.
    obs = models.CharField(db_column='Obs', max_length=150, blank=True, null=True)  # Field name made lowercase.
    texto = models.TextField(db_column='Texto', blank=True, null=True)  # Field name made lowercase. This field type is a guess.
    peso = models.FloatField(db_column='Peso', blank=True, null=True)  # Field name made lowercase.
    supcorp = models.FloatField(db_column='SupCorp', blank=True, null=True)  # Field name made lowercase.
    protocolo = models.CharField(db_column='Protocolo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    nciclo = models.CharField(db_column='NCiclo', max_length=5, blank=True, null=True)  # Field name made lowercase.
    aplicado = models.CharField(db_column='Aplicado', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'API_PrescreveQT'

    def __str__(self):
        return self.codpaciente


class ApiRadioterapia(models.Model):
    numpresc = models.CharField(primary_key=True, db_column='NumPresc', max_length=10)  # Field name made lowercase.
    codpaciente = models.CharField(db_column='CodPaciente', max_length=11, blank=True, null=True)  # Field name made lowercase.
    paciente = models.CharField(db_column='Paciente', max_length=200, blank=True, null=True)  # Field name made lowercase.
    codcidp = models.CharField(db_column='CodCidP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    estadio = models.CharField(db_column='Estadio', max_length=15, blank=True, null=True)  # Field name made lowercase.
    finalidade = models.CharField(db_column='Finalidade', max_length=20, blank=True, null=True)  # Field name made lowercase.
    intencaoradical = models.BooleanField(db_column='IntencaoRadical', blank=True, null=True)  # Field name made lowercase.
    intencaopaliativa = models.BooleanField(db_column='IntencaoPaliativa', blank=True, null=True)  # Field name made lowercase.
    tipot = models.CharField(db_column='TipoT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipon = models.CharField(db_column='TipoN', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipom = models.CharField(db_column='TipoM', max_length=10, blank=True, null=True)  # Field name made lowercase.
    naplicacoes = models.IntegerField(db_column='NAplicacoes', blank=True, null=True)  # Field name made lowercase.
    karno = models.CharField(db_column='Karno', max_length=5, blank=True, null=True)  # Field name made lowercase.
    codmed = models.CharField(db_column='CodMed', max_length=10, blank=True, null=True)  # Field name made lowercase.
    medico = models.CharField(db_column='Medico', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'API_Radioterapia'

    def __str__(self):
        return self.codpaciente


class ApiAplicMM_PrescQT(models.Model):
    idaplic = models.IntegerField(primary_key=True, db_column='IDAplic')  # Field name made lowercase.
    ndoc = models.CharField(db_column='NDoc', max_length=11, blank=True, null=True)  # Field name made lowercase.
    npresc = models.CharField(db_column='NPresc', max_length=11, blank=True, null=True)  # Field name made lowercase.
    codpaciente = models.CharField(db_column='CodPaciente', max_length=12, blank=True, null=True)  # Field name made lowercase.
    paciente = models.CharField(db_column='Paciente', max_length=200, blank=True, null=True)  # Field name made lowercase.
    hora = models.CharField(db_column='Hora', max_length=5, blank=True, null=True)  # Field name made lowercase.
    codproduto = models.CharField(db_column='CodProduto', max_length=10, blank=True, null=True)  # Field name made lowercase.
    brasindice = models.CharField(db_column='Brasindice', max_length=20, blank=True, null=True)  # Field name made lowercase.
    simpro = models.CharField(db_column='Simpro', max_length=20, blank=True, null=True)  # Field name made lowercase.
    descr = models.CharField(db_column='Descr', max_length=150, blank=True, null=True)  # Field name made lowercase.
    un = models.CharField(db_column='Un', max_length=10, blank=True, null=True)  # Field name made lowercase.
    quant = models.FloatField(db_column='Quant', blank=True, null=True)  # Field name made lowercase.
    codenf = models.CharField(db_column='CodEnf', max_length=10, blank=True, null=True)  # Field name made lowercase.
    enfermeiro = models.CharField(db_column='Enfermeiro', max_length=200, blank=True, null=True)  # Field name made lowercase.
    datahora = models.DateTimeField(db_column='DataHora', blank=True, null=True)  # Field name made lowercase.
    aplicado = models.CharField(db_column='Aplicado', max_length=10, blank=True, null=True)  # Field name made lowercase.
    grupop = models.CharField(db_column='GrupoP', max_length=200, blank=True, null=True)  # Field name made lowercase.
    diaquimioterapia = models.CharField(db_column='DiaQuimioterapia', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'API_AplicMM_PrescQT'

    def __str__(self):
        return self.npresc


class ApiAplicMM_PrescEletiva(models.Model):
    idaplic = models.IntegerField(primary_key=True, db_column='IDAplic')  # Field name made lowercase.
    ndoc = models.CharField(db_column='NDoc', max_length=11, blank=True, null=True)  # Field name made lowercase.
    npresc = models.CharField(db_column='NPresc', max_length=11, blank=True, null=True)  # Field name made lowercase.
    grupop = models.CharField(db_column='GrupoP', max_length=200, blank=True, null=True)  # Field name made lowercase.
    codpaciente = models.CharField(db_column='CodPaciente', max_length=12, blank=True, null=True)  # Field name made lowercase.
    paciente = models.CharField(db_column='Paciente', max_length=200, blank=True, null=True)  # Field name made lowercase.
    hora = models.CharField(db_column='Hora', max_length=5, blank=True, null=True)  # Field name made lowercase.
    codproduto = models.CharField(db_column='CodProduto', max_length=10, blank=True, null=True)  # Field name made lowercase.
    brasindice = models.CharField(db_column='Brasindice', max_length=20, blank=True, null=True)  # Field name made lowercase.
    simpro = models.CharField(db_column='Simpro', max_length=20, blank=True, null=True)  # Field name made lowercase.
    descr = models.CharField(db_column='Descr', max_length=150, blank=True, null=True)  # Field name made lowercase.
    un = models.CharField(db_column='Un', max_length=10, blank=True, null=True)  # Field name made lowercase.
    quant = models.DecimalField(db_column='Quant', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    codenf = models.CharField(db_column='CodEnf', max_length=10, blank=True, null=True)  # Field name made lowercase.
    enfermeiro = models.CharField(db_column='Enfermeiro', max_length=200, blank=True, null=True)  # Field name made lowercase.
    datahora = models.DateTimeField(db_column='DataHora', blank=True, null=True)  # Field name made lowercase.
    aplicado = models.CharField(db_column='Aplicado', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'API_AplicMM_PrescEletiva'

    def __str__(self):
        return self.npresc
        