import uuid
from django.db import models


class Cadpaciente(models.Model):
    codpaciente = models.CharField(db_column='CODPACIENTE', primary_key=True, max_length=10)  # Field name made lowercase.
    paciente = models.CharField(db_column='PACIENTE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sexo = models.CharField(db_column='SEXO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    datanasc = models.DateTimeField(db_column='DATANASC', blank=True, null=True)  # Field name made lowercase.
    idade = models.CharField(db_column='IDADE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rg = models.CharField(db_column='RG', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cpf = models.CharField(db_column='CPF', max_length=15, blank=True, null=True)  # Field name made lowercase.
    telefone2 = models.CharField(db_column='Telefone2', max_length=15, blank=True, null=True)  # Field name made lowercase.
    whatsapp = models.CharField(db_column='WhatsApp', max_length=15, blank=True, null=True)  # Field name made lowercase.
    datasist = models.DateTimeField(db_column='DataSist')

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
        return self.id


class ApiEnfevoluc(models.Model):
    ndoc = models.CharField(db_column='NDoc', max_length=11, primary_key=True)  # Field name made lowercase.
    codpaciente = models.ForeignKey(ApiEntrada, db_column='CodPaciente', max_length=11, on_delete=models.PROTECT)  # Field name made lowercase.
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
        return self.ndoc


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
    codpaciente = models.ForeignKey(ApiEntrada, db_column='CodPaciente', max_length=11, on_delete=models.PROTECT, related_name='prescqt_set')  # Field name made lowercase.
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
        return self.numero


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
        return self.numpresc


class ApiEntradaradio(models.Model):
    identradaradio = models.CharField(primary_key=True, db_column='idEntradaRadio', max_length=10)  # Field name made lowercase.
    codmovimento = models.CharField(db_column='CodMovimento', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codpaciente = models.CharField(db_column='CodPaciente', max_length=10, blank=True, null=True)  # Field name made lowercase.
    paciente = models.CharField(db_column='Paciente', max_length=200, blank=True, null=True)  # Field name made lowercase.
    numpresc = models.ForeignKey(ApiRadioterapia, db_column='NumPresc', max_length=10, on_delete=models.PROTECT, related_name='numpresc_set')  # Field name made lowercase.
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



class ApiAplicMM_PrescQT(models.Model):
    idaplic = models.IntegerField(primary_key=True, db_column='IDAplic')  # Field name made lowercase.
    ndoc = models.CharField(db_column='NDoc', max_length=11, blank=True, null=True)  # Field name made lowercase.
    npresc = models.ForeignKey(ApiPrescreveqt, db_column='NPresc', max_length=11, on_delete=models.PROTECT, related_name='npresc_set')  # Field name made lowercase.
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


class ApiPlanejfisicoc(models.Model):
    idplanejfisicoc = models.CharField(primary_key=True, db_column='idPlanejFisicoC', max_length=10)  # Field name made lowercase.
    codpaciente = models.CharField(db_column='CodPaciente', max_length=11, blank=True, null=True)  # Field name made lowercase.
    paciente = models.CharField(db_column='Paciente', max_length=200, blank=True, null=True)  # Field name made lowercase.
    numpresc = models.ForeignKey(ApiRadioterapia, db_column='NumPresc', max_length=10, on_delete=models.PROTECT, related_name='planej_set')  # Field name made lowercase.
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
        return self.idplanejfisicoc


class CadConvenio(models.Model):
    codconvenio = models.CharField(primary_key=True, db_column='CodConvenio', max_length=5)
    descr = models.CharField(db_column='Descr', max_length=100)
    hm = models.CharField(db_column='HM', max_length=5)

    class Meta:
        managed = False
        db_table = 'CadConvenio'

    def __str__(self):
        return str(self.codconvenio)


class Agenda(models.Model):
    idagenda = models.AutoField(primary_key=True, db_column='IDAgenda')
    codmedico = models.CharField(db_column='CodMedico', max_length=5)
    datahora = models.DateTimeField(db_column='DataHora')
    nome = models.CharField(db_column='Nome', max_length=250)
    codconvenio = models.ForeignKey(CadConvenio, db_column='CodConvenio', max_length=5, on_delete=models.PROTECT)
    codpaciente = models.ForeignKey(Cadpaciente, db_column='CodPaciente', on_delete=models.PROTECT)
    obs = models.CharField(db_column='Obs', max_length=200)
    usuario = models.CharField(db_column='Usuario', max_length=100, blank=True, null=True)
    descr = models.CharField(db_column='Descr', max_length=100, default='')
    datasist = models.DateTimeField(db_column='DataSist') 
    numero = models.CharField(db_column='Numero', max_length=20, default='')
    endereco = models.CharField(db_column='Endereco', max_length=200, default='')
    cidade = models.CharField(db_column='Cidade', max_length=100, default='')
    cep = models.CharField(db_column='Cep', max_length=20, default='')
    cpf = models.CharField(db_column='CPF', max_length=20, default='')
    estado = models.CharField(db_column='Estado', max_length=20, default='')
    cemarc = models.CharField(db_column='Cemarc', max_length=20, default='')
    confatd = models.CharField(db_column='ConfAtd', max_length=2, blank=True, null=True)
    bairro = models.CharField(db_column='Bairro', max_length=20, default='')
    profissao = models.CharField(db_column='PROFISSAO', max_length=20, default='')
    sexo = models.CharField(db_column='Sexo', max_length=20, default='')
    ec = models.CharField(db_column='EC', max_length=20, default='')
    oe = models.CharField(db_column='OE', max_length=20, default='')
    filiacao = models.CharField(db_column='Filiacao', max_length=20, default='')
    rg = models.CharField(db_column='RG', max_length=20, default='')
    retorno = models.CharField(db_column='Retorno', max_length=20, default='N')
    tipo = models.CharField(db_column='Tipo', max_length=5)
    matricula = models.CharField(db_column='Matricula', max_length=20, default='')
    plano = models.CharField(db_column='Plano', max_length=20, default='')
    telefone = models.CharField(db_column='Telefone', max_length=20, default='')
    grupoemp = models.CharField(db_column='GrupoEmp', max_length=2, default='01')
    filial = models.CharField(db_column='Filial', max_length=2, default='01')
    ordem = models.CharField(db_column='Ordem', max_length=2, default='0')
    senha = models.CharField(db_column='Senha', max_length=12, default='')
    reconvoca = models.CharField(db_column='Reconvoca', max_length=20, default='')
    codmovimento = models.CharField(db_column='CodMovimento', max_length=50, blank=True, null=True)
    ntratradio = models.IntegerField(db_column='Ntratradio')
    celular = models.CharField(db_column='Celular', max_length=20, default='')
    datanasc2 = models.DateTimeField(db_column='DataNasc2')
    email = models.CharField(db_column='EMail', max_length=50, default='')
    local = models.CharField(db_column='Local', max_length=50, default='')
    planejado = models.CharField(db_column='Planejado', max_length=5)
    whatsapp = models.CharField(db_column='WhatsApp', max_length=11)
    tipooriginal = models.CharField(db_column='TipoOriginal', max_length=10)

    class Meta:
        managed = False
        db_table = 'Agenda'

    def __str__(self):
        return str(self.idagenda)


class Entrada(models.Model):    
    codmovimento = models.CharField(db_column='CodMovimento', primary_key=True, max_length=10)
    codpaciente = models.ForeignKey(Cadpaciente ,db_column='CodPaciente', max_length=10, on_delete=models.PROTECT)
    codconvenio = models.ForeignKey(CadConvenio, db_column='CodConvenio', max_length=6, on_delete=models.PROTECT)
    matricula = models.CharField(db_column='Matricula', max_length=30, blank=True, null=True)
    tipo = models.CharField(db_column='Tipo', max_length=25, blank=True, null=True) 
    datahoraent = models.DateTimeField(db_column='DataHoraEnt', blank=True, null=True)
    hist = models.CharField(db_column='Hist', max_length=200, blank=True, null=True) 
    codmedico = models.CharField(db_column='CodMedico', max_length=6, blank=True, null=True)
    local = models.CharField(db_column='Local', max_length=20, blank=True, null=True)
    recep = models.CharField(db_column='Recep', max_length=20, default='API')
    total = models.FloatField(db_column='Total', blank=True, null=True) 
    fechado = models.CharField(db_column='Fechado', max_length=20) 
    codamb = models.CharField(db_column='CodAmb', max_length=15)
    consultaok = models.CharField(db_column='ConsultaOk', max_length=5, blank=True, null=True)
    restrito = models.CharField(db_column='Restrito', max_length=15, default='N')
    obito = models.CharField(db_column='Obito', max_length=15, default='')
    deposito = models.IntegerField(db_column='Deposito', default=0)
    codsolic = models.CharField(db_column='CodSolic', max_length=15, default='')
    medsolic = models.CharField(db_column='Medsolic', max_length=15, default='')
    usuario = models.CharField(db_column='Usuario', max_length=20, blank=True, null=True)  
    datasist = models.DateTimeField(db_column='DataSist')  
    datahoraagd = models.CharField(db_column='DataHoraAgd', max_length=30, default='  /  /       :  ')
    interno = models.CharField(db_column='Interno', max_length=15, default='Ext')
    pacote = models.CharField(db_column='Pacote', max_length=15, default='')
    nd = models.IntegerField(db_column='ND', default=0)
    entrega = models.CharField(db_column='Entrega', max_length=30, default='  /  /       :  ')
    eletiva = models.CharField(db_column='Eletiva', max_length=15, default='E')
    codant = models.CharField(db_column='CodAnt', max_length=15, default='13.4.130')
    recebido = models.CharField(db_column='Recebido', max_length=15, default='N')
    obs = models.CharField(db_column='Obs', max_length=15, default='')
    recup = models.CharField(db_column='Recup', max_length=15, default='')
    origem = models.CharField(db_column='Origem', max_length=15, default='108')
    npedlab = models.IntegerField(db_column='Npedlab', default=0)
    glosa = models.IntegerField(db_column='Glosa', default=0)
    plano = models.CharField(db_column='Plano', max_length=15, default='')
    tabhm = models.CharField(db_column='TabHM', max_length=5, blank=True, null=True)
    numrestr = models.IntegerField(db_column='Numrestr', default=0)    
    grupoemp = models.CharField(db_column='GrupoEmp', max_length=2, default='01') 
    filial = models.CharField(db_column='Filial', max_length=2, default='01')
    entemerg = models.CharField(db_column='EntEmerg', max_length=15, default='')
    ordem = models.CharField(db_column='Ordem', max_length=15, default='')
    prefere = models.CharField(db_column='Prefere', max_length=15, default='9')
    tipoatend = models.CharField(db_column='TipoAtend', max_length=15, default='4')
    tiposaida = models.CharField(db_column='TipoSaida', max_length=15, default='5')
    tipoconsulta = models.CharField(db_column='Tipoconsulta', max_length=15, default='')
    guiaprincipal = models.CharField(db_column='GuiaPrincipal', max_length=15, default='')
    condguia = models.CharField(db_column='CondGuia', max_length=15, default='N')
    codexp = models.CharField(db_column='CodExp', max_length=15, default='')
    triagem = models.CharField(db_column='Triagem', max_length=15, default='9')
    tipotiss = models.CharField(db_column='TipoTiss', max_length=15, default='3')
    tiss28 = models.CharField(db_column='Tiss28', max_length=15, default='3')
    chklistpqa = models.CharField(db_column='ChkListpqa', max_length=15, default='PARCIAL')
    datahoraint = models.DateTimeField(db_column='DataHoraInt')
    loteent = models.CharField(db_column='LoteEnt', max_length=15, default='001L01')
    valcota = models.IntegerField(db_column='Valcota', default=0)
    localini = models.CharField(db_column='Localini', max_length=15, default='')
    natendimento = models.CharField(db_column='Natendimento', max_length=15)
    datamarcada = models.DateTimeField(db_column='DataMarcada')
    tipoatend2 = models.CharField(db_column='Tipoatend2', max_length=2, default='4')
    codespec = models.CharField(db_column='CodEspec', max_length=2, default='197')
    idsenhaatd = models.IntegerField(db_column='IDSenhaATD', default=0)
    guia = models.CharField(db_column='Guia', max_length=30, default='')
    prontuario = models.CharField(db_column='Prontuario', max_length=30, default='')
    acomod = models.CharField(db_column='Acomod', max_length=30, default='') 
    codcid = models.CharField(db_column='CodCid', max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Entrada'

    def __str__(self):
        return self.codmovimento


class Radioterapia(models.Model):
    numpresc = models.CharField(primary_key=True, db_column='NumPresc', max_length=10)  # Field name made lowercase.
    codpaciente = models.ForeignKey(Cadpaciente, db_column='CodPaciente', max_length=11, on_delete=models.PROTECT)
    codcidp = models.CharField(db_column='CodCidP', max_length=10, blank=True, null=True)  # Field name made lowercase.
    estadio = models.CharField(db_column='Estadio', max_length=15, blank=True, null=True)  # Field name made lowercase.
    finalidade = models.CharField(db_column='Finalidade', max_length=20, blank=True, null=True)  # Field name made lowercase.
    intencaoradical = models.BooleanField(db_column='IntencaoRadical', blank=True, null=True)  # Field name made lowercase.
    intencaopaliativa = models.BooleanField(db_column='IntencaoPaliativa', blank=True, null=True)  # Field name made lowercase.
    tipot = models.CharField(db_column='TipoT', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipon = models.CharField(db_column='TipoN', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipom = models.CharField(db_column='TipoM', max_length=10, blank=True, null=True)  # Field name made lowercase.
    naplicacoes = models.IntegerField(db_column='NAplicacoes', blank=True, null=True)  # Field name made lowercase.
    ntratamento = models.IntegerField(db_column='NTratamento', blank=True, null=True)  # Field name made lowercase.
    idradio = models.IntegerField(db_column='idRadio', blank=True, null=True)  # Field name made lowercase.
    karno = models.CharField(db_column='Karno', max_length=5, blank=True, null=True)  # Field name made lowercase.
    codmed = models.CharField(db_column='CodMed', max_length=10, blank=True, null=True)
    tratado = models.CharField(db_column='Tratado', max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Radioterapia'

    def __str__(self):
        return str(self.numpresc)


class Entradaradio(models.Model):
    codmovimento = models.CharField(db_column='CodMovimento', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codpaciente = models.CharField(db_column='CodPaciente', max_length=10, blank=True, null=True)  # Field name made lowercase.
    numpresc = models.ForeignKey(Radioterapia, db_column='NumPresc', max_length=10, on_delete=models.PROTECT, related_name='numpresc_set')  # Field name made lowercase.
    idplanejfisico = models.CharField(db_column='idPlanejFisico', max_length=10, blank=True, null=True)  # Field name made lowercase.
    encerrado = models.CharField(db_column='Encerrado', max_length=10, blank=True, null=True)  # Field name made lowercase.
    observacao = models.CharField(db_column='Observacao', max_length=200, blank=True, null=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=20, blank=True, null=True)  # Field name made lowercase.
    datahora = models.DateTimeField(db_column='DataHora', blank=True, null=True)  # Field name made lowercase.
    datasist = models.DateTimeField(db_column='DataSist', blank=True, null=True)  # Field name made lowercase.
    nplanejamento = models.IntegerField(db_column='NPlanejamento', blank=True, null=True)  # Field name made lowercase.
    nomecampo = models.CharField(db_column='NomeCampo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    incidencia = models.CharField(db_column='Incidencia', max_length=50, blank=True, null=True)  # Field name made lowercase.
    grupoemp = models.CharField(db_column='GrupoEmp', max_length=2, blank=True, null=True)  # Field name made lowercase.
    filial = models.CharField(db_column='Filial', max_length=2, blank=True, null=True)  # Field name made lowercase.
    ntratamento = models.IntegerField(db_column='NTratamento', blank=True, null=True)  # Field name made lowercase.
    ncampo = models.IntegerField(db_column='NCampo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EntradaRadio'

    def __str__(self):
        return self.codmovimento


class Planejfisicoc(models.Model):
    # Quando o Django precisa inserir registros novos no banco,
    # A coluna chave primária precisa ser do tipo models.AutoField.
    # Dessa forma, quem atribui um valor para a coluna, é o próprio banco, e não o Django.
    # Evitando assim o erro de inserir valor explícito em uma coluna com IDENTITY INSERT ON. =)
    idplanejfisicoc = models.AutoField(primary_key=True, db_column='idPlanejFisicoC', editable=False)  # Field name made lowercase.
    codpaciente = models.ForeignKey(Cadpaciente, db_column='CodPaciente', max_length=11, on_delete=models.PROTECT)  # Field name made lowercase.
    codmovimento = models.CharField(db_column='CodMovimento', max_length=11)  # Field name made lowercase.
    numpresc = models.ForeignKey(Radioterapia, db_column='NumPresc', max_length=10, on_delete=models.PROTECT)  # Field name made lowercase.
    energia = models.CharField(db_column='Energia', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dtt = models.CharField(db_column='DTT', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dtd = models.CharField(db_column='DTD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    naplicacoes = models.IntegerField(db_column='NAplicacoes', blank=True, null=True)  # Field name made lowercase.
    datasist = models.DateTimeField(db_column='DataSist')
    ativo = models.CharField(db_column='Ativo', max_length=5)
    unidade_monitora = models.CharField(db_column='DoseMonitor', max_length=20, blank=True, null=True)  # Field name made lowercase.
    nplanejamento = models.IntegerField(db_column='NPlanejamento', blank=True, null=True)  # Field name made lowercase.
    ntratamento = models.IntegerField(db_column='NTratamento', blank=True, null=True)  # Field name made lowercase.
    locanatomica = models.CharField(db_column='LocAnatomica', max_length=250)
    ncampo = models.IntegerField(db_column='NCampo', blank=True, null=True)  # Field name made lowercase.
    ordemcampo = models.IntegerField(db_column='OrdemCampo', blank=True, null=True)  # Field name made lowercase.
    iniciotrat = models.IntegerField(db_column='InicioTrat', blank=True, null=True)  # Field name made lowercase.
    incidencia = models.CharField(db_column='Incidencia', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tpfeixe = models.CharField(db_column='TpFeixe', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fase = models.IntegerField(db_column='Fase', blank=True, null=True)  # Field name made lowercase.
    aparelho = models.CharField(db_column='Aparelho', max_length=20, default='ACELERADOR LINEAR')  # Field name made lowercase.
    tamanhocampos = models.CharField(db_column='TamanhoCampos', max_length=5, default='0')  # Field name made lowercase.
    campoequivapente = models.CharField(db_column='CampoEquivalente', max_length=5, default='0')  # Field name made lowercase.
    campocolimado = models.CharField(db_column='CampoColimado', max_length=5, default='0')  # Field name made lowercase.
    distsuperficie = models.CharField(db_column='DistSuperficie', max_length=5, default='0')  # Field name made lowercase.
    distisocentro = models.CharField(db_column='DistIsocentro', max_length=5, default='0')  # Field name made lowercase.
    profundidade = models.CharField(db_column='Profundidade', max_length=5, default='0')  # Field name made lowercase.
    doseprofunda = models.CharField(db_column='DoseProfunda', max_length=5, default='0')  # Field name made lowercase.
    razaotecido = models.CharField(db_column='RazaoTecido', max_length=5, default='0')  # Field name made lowercase.
    dosemaxcampo = models.CharField(db_column='DoseMaxCampo', max_length=5, default='0')  # Field name made lowercase.
    rendimento = models.CharField(db_column='Rendimento', max_length=5, default='0')  # Field name made lowercase.
    fatcalibracao = models.CharField(db_column='FatCalibracao', max_length=5, default='0')  # Field name made lowercase.
    fatbandeja = models.CharField(db_column='FatBandeja', max_length=5, default='0')  # Field name made lowercase.
    fatfiltro = models.CharField(db_column='FatFiltro', max_length=5, default='0')  # Field name made lowercase.
    fatdistancia = models.CharField(db_column='FatDistancia', max_length=5, default='0')  # Field name made lowercase.
    RendPinal = models.CharField(db_column='RendPinal', max_length=5, default='0')  # Field name made lowercase.
    tempaplicacao = models.CharField(db_column='TempAplicacao', max_length=5, default='0')  # Field name made lowercase.
    grupoemp = models.CharField(db_column='GrupoEmp', max_length=5, default='01')  # Field name made lowercase.
    filial = models.CharField(db_column='Filial', max_length=5, default='01')  # Field name made lowercase.
    fatrendimento = models.CharField(db_column='FatRendimento', max_length=5, default='0')  # Field name made lowercase.
    portal = models.CharField(db_column='Portal', max_length=5, default='0')  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=30)
    id_mosaiq = models.IntegerField(db_column='ID_MOSAIQ')

    class Meta:
        managed = False
        db_table = 'PlanejFisicoC'

    def __str__(self):
        return str(self.codpaciente)

    # def save(self, *args, **kwargs):
    #     if self.idplanejfisicoc:
    #         self._meta.local_fields = [f for f in self._meta.local_fields if f.name != 'idplanejfisicoc']
    #         super().save(*args, **kwargs)


class Planejfisico(models.Model):
    idplanejfisico = models.AutoField(primary_key=True, db_column='idPlanejFisico')  # Field name made lowercase.
    idplanejfisicoc = models.ForeignKey(Planejfisicoc, db_column='idPlanejFisicoC', on_delete=models.PROTECT)  # Field name made lowercase.
    codpaciente = models.ForeignKey(Cadpaciente, db_column='CodPaciente', max_length=11, on_delete=models.PROTECT)  # Field name made lowercase.
    codmovimento = models.CharField(db_column='CodMovimento', max_length=11)  # Field name made lowercase.
    numpresc = models.ForeignKey(Radioterapia, db_column='NumPresc', max_length=10, on_delete=models.PROTECT, related_name='planej_set2')  # Field name made lowercase.
    incidencia = models.CharField(db_column='Incidencia', max_length=50, blank=True, null=True)  # Field name made lowercase.
    energia = models.CharField(db_column='Energia', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tecnica = models.CharField(db_column='Tecnica', max_length=10, blank=True, null=True)  # Field name made lowercase.
    unidade_monitora = models.CharField(db_column='UnMonitoracao', max_length=20, blank=True, null=True)  # Field name made lowercase.
    angulacao = models.CharField(db_column='Angulacao', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nomecampo = models.CharField(db_column='NomeCampo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    nplanejamento = models.IntegerField(db_column='NPlanejamento', blank=True, null=True)  # Field name made lowercase.
    ntratamento = models.IntegerField(db_column='NTratamento', blank=True, null=True)  # Field name made lowercase.
    ncampo = models.IntegerField(db_column='NCampo', blank=True, null=True)  # Field name made lowercase.
    fase = models.IntegerField(db_column='Fase', blank=True, null=True)  # Field name made lowercase.
    ativo = models.CharField(db_column='Ativo', max_length=5)
    aparelho = models.CharField(db_column='Aparelho', default='ACELERADOR LINEAR', max_length=20)
    distanciafonte = models.CharField(db_column='DistanciaFonte', default='0', max_length=5)
    tamanhocampo = models.CharField(db_column='TamanhoCampo', default='', max_length=5)
    tempoalicacao = models.CharField(db_column='TempoAlicacao', default='0', max_length=5)
    datasist = models.DateTimeField(db_column='DataSist')
    grupoemp = models.CharField(db_column='GrupoEmp', default='01', max_length=2)
    filial = models.CharField(db_column='Filial', default='01', max_length=2)
    obs = models.CharField(db_column='Obs', default='', max_length=5)
    bandeja = models.CharField(db_column='Bandeja', default='', max_length=5)
    checacampo = models.CharField(db_column='ChecaCampo', default='0', max_length=5)
    tratado = models.CharField(db_column='Tratado', default='NAO', max_length=5)
    suportedecabeca = models.CharField(db_column='SuporteDeCabeca', default='', max_length=5)
    abridordeboca = models.CharField(db_column='AbridorDeBoca', default='0', max_length=5)
    baset = models.CharField(db_column='BaseT', default='0', max_length=5)
    bolus = models.CharField(db_column='Bolus', default='0', max_length=5)
    extensordemesa = models.CharField(db_column='ExtensorDeMesa', default='0', max_length=5)
    hemibloqueador = models.CharField(db_column='HemiBloqueador', default='0', max_length=5)
    mascara = models.CharField(db_column='Mascara', default='0', max_length=5)
    moldepersonalizado = models.CharField(db_column='MoldePersonalizado', default='0', max_length=5)
    rampademama = models.CharField(db_column='RampaDeMama', default='0', max_length=5)
    suportedeface = models.CharField(db_column='SuporteDeFace', default='0', max_length=5)
    suportedeperna = models.CharField(db_column='SuporteDePerna', default='0', max_length=5)
    vaclock = models.CharField(db_column='VacLock', default='0', max_length=5)
    bolusdetalhe = models.CharField(db_column='BolusDetalhe', default='', max_length=5)
    basetdetalhe = models.CharField(db_column='BaseTDetalhe', default='', max_length=5)
    retratordeombrodetalhe = models.CharField(db_column='RetratorDeOmbroDetalhe', default='', max_length=5)
    suportedefacedetalhe = models.CharField(db_column='SuporteDeFaceDetalhe', default='', max_length=5)
    suportedepernadetalhe = models.CharField(db_column='SuporteDePernaDetalhe', default='', max_length=5)
    isopor = models.CharField(db_column='Isopor', default='0', max_length=5)
    baseuniversal = models.CharField(db_column='BaseUniversal', default='0', max_length=5)
    suportedepes = models.CharField(db_column='SuporteDePes', default='', max_length=5)
    rampademapadetalhe = models.CharField(db_column='RampaDeMamaDetalhe', default='', max_length=5)
    dtt = models.CharField(db_column='DTT', max_length=50, blank=True, null=True)
    dtd = models.CharField(db_column='DTD', max_length=100, blank=True, null=True)   
    usuario = models.CharField(db_column='Usuario', max_length=30)
    id_mosaiq = models.IntegerField(db_column='ID_MOSAIQ')

    class Meta:
        managed = False
        db_table = 'PlanejFisico'

    def __str__(self):
        return str(self.ncampo)


class PrescrRadio(models.Model):
    idprescrradio = models.AutoField(primary_key=True, db_column='idPrescrRadio')
    idradio = models.IntegerField(db_column='idRadio')
    ncampos = models.IntegerField(db_column='NCampos')
    codmovimento = models.CharField(db_column='CodMovimento', max_length=11)
    locanatomica = models.CharField(db_column='LocAnatomica', max_length=100)
    prof = models.CharField(db_column='Prof', max_length=5, default='')
    datasist = models.DateTimeField(db_column='DataSist')
    grupoemp = models.CharField(db_column='GrupoEmp', max_length=2, default='01')
    filial = models.CharField(db_column='Filial', max_length=2, default='01')
    numpresc = models.ForeignKey(Radioterapia, db_column='NumPresc', on_delete=models.PROTECT)
    incidencia = models.CharField(db_column='Incidencia', max_length=20)
    naplicacoes = models.IntegerField(db_column='NAplicacoes')
    portal = models.IntegerField(db_column='Portal', default=5)
    ntratamento = models.IntegerField(db_column='NTratamento')
    tratado = models.CharField(db_column='Tratado', max_length=3, default='NAO')
    iniciotrat = models.IntegerField(db_column='InicioTrat')
    codpaciente = models.ForeignKey(Cadpaciente, db_column='CodPaciente', on_delete=models.PROTECT)
    nrestudo = models.IntegerField(db_column='NReestudo', default=0)
    usuario = models.CharField(db_column='Usuario', max_length=100, default='API')
    energia = models.CharField(db_column='Energia', max_length=7)
    tecnica = models.CharField(db_column='Tecnica', max_length=20)
    tpfeixe = models.CharField(db_column='TpFeixe', max_length=20)
    dosettotal = models.IntegerField(db_column='DoseTTotal')
    dosetdiaria = models.IntegerField(db_column='DoseTDiaria')
    fase = models.IntegerField(db_column='Fase')
    id_mosaiq = models.IntegerField(db_column='ID_MOSAIQ')

    class Meta:
        managed = False
        db_table = 'PrescrRadio'
    
    def __str__(self):
        return str(self.idprescrradio)


class SolicExa(models.Model):
    nsolic = models.IntegerField(db_column='NSolic')
    codpaciente = models.CharField(db_column='CodPaciente', max_length=11)
    codamb = models.CharField(db_column='CodAmb', max_length=15)
    descr = models.CharField(db_column='Descr', max_length=500)
    codmedico = models.CharField(db_column='CodMedico', max_length=5)
    tipo = models.CharField(db_column='Tipo', max_length=10)
    datasist = models.DateTimeField(db_column='DataSist')
    codcid = models.CharField(db_column='CodCid', max_length=10)
    grupoemp = models.CharField(db_column='GrupoEmp', max_length=2)
    filial = models.CharField(db_column='Filial', max_length=2)
    quant = models.IntegerField(db_column='Quant')
    codpacref = models.CharField(db_column='CodPacRef', max_length=11)
    item = models.AutoField(primary_key=True, db_column='Item')
    codconvenio = models.CharField(db_column='CodConvenio', max_length=5)
    npresc = models.ForeignKey(Radioterapia, db_column='NumeroPrescricao', on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'SolicExa'
    
    def __str__(self):
        return str(self.codamb)


class Fatura(models.Model):
    codpaciente = models.CharField(db_column='CodPaciente', max_length=11)
    grupo = models.CharField(db_column='Grupo', max_length=5)
    codtaxa = models.CharField(db_column='CodTaxa', max_length=15)
    chave = models.CharField(db_column='Chave', max_length=15, default='')
    descr = models.CharField(db_column='Descr', max_length=500)
    data = models.DateTimeField(db_column='Data')
    valor = models.FloatField(db_column='Valor', max_length=15)
    quant = models.IntegerField(db_column='Quant')
    filme = models.IntegerField(db_column='Filme', default=0)
    codmedico = models.CharField(db_column='CodMedico', max_length=5)
    datasist = models.DateTimeField(db_column='DataSist')
    usuario = models.CharField(db_column='Usuario', max_length=20, default='API')
    codamb = models.CharField(db_column='CodAmb', max_length=15)
    ch = models.FloatField(db_column='Ch', max_length=15)
    un = models.CharField(db_column='Un', max_length=10, default='')
    custoop = models.IntegerField(db_column='CustoOp', default=0)
    local = models.CharField(db_column='Local', max_length=10, default='112')
    grupoimp = models.CharField(db_column='GrupoImp', max_length=10, default='112')
    valorp = models.FloatField(db_column='ValorP', max_length=15, default=0)
    honor = models.FloatField(db_column='Honor', max_length=15)
    med = models.FloatField(db_column='Med', max_length=15, default=0)
    mat = models.FloatField(db_column='Mat', max_length=15, default=0)
    diaria = models.FloatField(db_column='Diaria', max_length=15, default=0)
    taxa = models.FloatField(db_column='Taxa', max_length=15, default=0)
    gas = models.FloatField(db_column='Gas', max_length=15, default=0)
    vprof = models.FloatField(db_column='VProf', max_length=15, default=0)
    voutros = models.FloatField(db_column='VOutros', max_length=15, default=0)
    valponto = models.FloatField(db_column='ValPonto', max_length=15, default=0)
    ptosadt = models.FloatField(db_column='PtoSadt', max_length=15, default=0)
    vpprof = models.FloatField(db_column='VpProf', max_length=15)
    diaapt = models.FloatField(db_column='DiaApt', max_length=15, default=0)
    diauti = models.FloatField(db_column='DiaUti', max_length=15, default=0)
    diaenf = models.FloatField(db_column='DiaEnf', max_length=15, default=0)
    obs = models.CharField(db_column='Obs', max_length=500)
    custo = models.FloatField(db_column='Custo', max_length=15, default=0)
    glosa = models.FloatField(db_column='Glosa', max_length=15, default=0)
    numaux = models.CharField(db_column='NumAux', max_length=10, default='10')
    codaux = models.CharField(db_column='CodaUX', max_length=10, default='EXA')
    prodrep = models.CharField(db_column='ProdRep', max_length=5, default='N')
    grupoemp = models.CharField(db_column='GrupoEmp', max_length=2, default='01')
    filial = models.CharField(db_column='Filial', max_length=2, default='01')
    codmedemp = models.CharField(db_column='CodMedEmp', max_length=5, default='')
    cota = models.IntegerField(db_column='Cota', default=1)
    usuposto = models.CharField(db_column='UsuPosto', max_length=5, default='')
    graumedico = models.CharField(db_column='GrauMedico', max_length=5, default='')
    tabtiss = models.CharField(db_column='TabTiss', max_length=5, default='')
    tipoacomod = models.CharField(db_column='TipoAcomod', max_length=5, default='N')
    codtiss = models.CharField(db_column='CodTiss', max_length=5, default='')
    viaacesso = models.CharField(db_column='ViaAcesso', max_length=5, default='')
    tecutiliz = models.CharField(db_column='TecUtilIZ', max_length=5, default='')
    localac = models.CharField(db_column='LocalAC', max_length=5, default='112')
    valoracresc = models.FloatField(db_column='ValorAcresc', max_length=15, default=0)
    opm = models.FloatField(db_column='OPM', max_length=15, default=0)
    qtdsolic = models.IntegerField(db_column='QtdSolic', default=1)
    codgasto = models.IntegerField(db_column='CodGasto', default=0)
    dente = models.CharField(db_column='Dente', max_length=5, default='')
    regiaodente = models.CharField(db_column='RegiaoDente', max_length=5, default='')
    face = models.CharField(db_column='Face', max_length=5, default='')
    seq = models.AutoField(primary_key=True, db_column='Seq')
    cbo = models.CharField(db_column='CBO', max_length=5, default='')
    itempresc = models.CharField(db_column='ItemPresc', max_length=5, default='')
    npresc = models.IntegerField(db_column='NPresc', default=0)
    hora = models.CharField(db_column='Hora', max_length=5, default='')
    vrepasse = models.FloatField(db_column='VRepasse', max_length=15, default=0)
    qtdtiss = models.IntegerField(db_column='QtdTiss', default=1)
    grupoproc = models.CharField(db_column='GrupoProc', max_length=5, default='')
    codtuss = models.CharField(db_column='CodTuss', max_length=5, default='')
    codtus = models.CharField(db_column='CodTus', max_length=5, default='')
    codproprio = models.CharField(db_column='CodProprio', max_length=5, default='')
    unproprio = models.CharField(db_column='UnProprio', max_length=5, default='')

    class Meta:
        managed = False
        db_table = 'Fatura'
    
    def __str__(self):
        return str(self.seq)


class Exame(models.Model):
    idexame = models.AutoField(primary_key=True, db_column='IDExame')
    codpaciente = models.CharField(db_column='CodPaciente', max_length=11)
    codamb = models.CharField(db_column='CodAmb', max_length=15)
    local = models.CharField(db_column='Local', max_length=10, default='112')
    descr = models.CharField(db_column='Descr', max_length=500)
    ok = models.CharField(db_column='Ok', max_length=5, default='')
    quant = models.IntegerField(db_column='Quant')
    codmedico = models.CharField(db_column='CodMedico', max_length=5)
    interno = models.CharField(db_column='Interno', max_length=5, default='Ext')
    contexa = models.CharField(db_column='ContExa', max_length=5, default='1')
    usuario = models.CharField(db_column='Usuario', max_length=20, default='API')
    datasist = models.DateTimeField(db_column='DataSist')
    chave = models.CharField(db_column='Chave', max_length=11)
    medcred = models.CharField(db_column='MedCred', max_length=2, default='N')
    valor = models.FloatField(db_column='Valor', max_length=15)
    etiq = models.CharField(db_column='Etiq', max_length=5, default='')
    solic = models.CharField(db_column='Solic', max_length=5, default='')
    guia = models.CharField(db_column='Guia', max_length=5, default='')
    senha = models.CharField(db_column='Senha', max_length=5, default='')
    tipo = models.CharField(db_column='Tipo', max_length=5, default='R')
    codigo = models.IntegerField(db_column='Codigo')
    dataproc = models.DateTimeField(db_column='DataProc')
    codsolic = models.CharField(db_column='CodSolic', max_length=5, default='')
    autoriza = models.CharField(db_column='Autoriza', max_length=5, default='N')
    grupoemp = models.CharField(db_column='GrupoEmp', max_length=5, default='01')
    filial = models.CharField(db_column='Filial', max_length=5, default='01')
    numaux = models.CharField(db_column='NumAux', max_length=5, default='1')
    modalidade = models.CharField(db_column='Modalidade', max_length=5, default='')
    codpacref = models.ForeignKey(Cadpaciente, db_column='CodPacRef', max_length=10, on_delete=models.PROTECT)
    codtus = models.CharField(db_column='CodTus', max_length=5, default='')
    cbosus = models.CharField(db_column='CBOSus', max_length=5, default='')
    statusconsulta = models.CharField(db_column='Statusconsulta', max_length=5, default='')
    grupoproc = models.CharField(db_column='GrupoProc', max_length=5, default='')

    class Meta:
        managed = False
        db_table = 'Exame'
    
    def __str__(self):
        return str(self.idexame)


class TabAmb(models.Model):
    codconvenio = models.ForeignKey(CadConvenio, db_column='CodConvenio', on_delete=models.PROTECT)
    codamb = models.CharField(db_column='CodAmb', max_length=10)
    descr = models.CharField(db_column='Descr', max_length=800)
    ch = models.IntegerField(db_column='CH')
    chanest = models.IntegerField(db_column='CHAnest')

    class Meta:
        managed = False
        db_table = 'TabAmb'
    
    def __str__(self):
        return str(self.id)