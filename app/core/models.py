# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cadpaciente(models.Model):
    codpaciente = models.CharField(db_column='CODPACIENTE', primary_key=True, max_length=10)  # Field name made lowercase.
    paciente = models.CharField(db_column='PACIENTE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    sexo = models.CharField(db_column='SEXO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    datanasc = models.DateTimeField(db_column='DATANASC', blank=True, null=True)  # Field name made lowercase.
    naturalidade = models.CharField(db_column='NATURALIDADE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cpf = models.CharField(db_column='CPF', max_length=15, blank=True, null=True)  # Field name made lowercase.
    endereco = models.CharField(db_column='ENDERECO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    bairro = models.CharField(db_column='BAIRRO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cidade = models.CharField(db_column='CIDADE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='ESTADO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    datasist = models.DateTimeField(db_column='DATASIST', blank=True, null=True)  # Field name made lowercase.
    codconvenio = models.CharField(db_column='CODCONVENIO', max_length=3, blank=True, null=True)  # Field name made lowercase.
    profissao = models.CharField(db_column='PROFISSAO', max_length=200, blank=True, null=True)  # Field name made lowercase.
    idade = models.CharField(db_column='IDADE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    rg = models.CharField(db_column='RG', max_length=20, blank=True, null=True)  # Field name made lowercase.
    oe = models.CharField(db_column='OE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    cep = models.CharField(db_column='CEP', max_length=15, blank=True, null=True)  # Field name made lowercase.
    telefone = models.CharField(db_column='TELEFONE', max_length=100, blank=True, null=True)  # Field name made lowercase.
    matricula = models.CharField(db_column='MATRICULA', max_length=30, blank=True, null=True)  # Field name made lowercase.
    titular = models.CharField(db_column='TITULAR', max_length=100, blank=True, null=True)  # Field name made lowercase.
    resp = models.CharField(db_column='RESP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    end_resp = models.CharField(db_column='END_RESP', max_length=100, blank=True, null=True)  # Field name made lowercase.
    plano = models.CharField(db_column='PLANO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    quant = models.IntegerField(db_column='QUANT', blank=True, null=True)  # Field name made lowercase.
    ult_vez = models.DateTimeField(db_column='ULT_VEZ', blank=True, null=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='USUARIO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ec = models.CharField(db_column='EC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    validade = models.CharField(db_column='VALIDADE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    ultpagto = models.CharField(db_column='ULTPAGTO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    md = models.CharField(db_column='MD', max_length=1, blank=True, null=True)  # Field name made lowercase.
    mesnasc = models.IntegerField(db_column='MESNASC', blank=True, null=True)  # Field name made lowercase.
    peso = models.CharField(db_column='PESO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    altura = models.CharField(db_column='ALTURA', max_length=10, blank=True, null=True)  # Field name made lowercase.
    datanascr = models.CharField(db_column='DATANASCR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    medico = models.CharField(db_column='MEDICO', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nome = models.CharField(db_column='NOME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    filiacao = models.CharField(db_column='FILIACAO', max_length=150, blank=True, null=True)  # Field name made lowercase.
    tipodoc = models.CharField(db_column='TIPODOC', max_length=1, blank=True, null=True)  # Field name made lowercase.
    codmun = models.CharField(db_column='CODMUN', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codmed = models.CharField(db_column='CODMED', max_length=3, blank=True, null=True)  # Field name made lowercase.
    numero = models.CharField(db_column='NUMERO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    telresp = models.CharField(db_column='TELRESP', max_length=50, blank=True, null=True)  # Field name made lowercase.
    barra = models.CharField(db_column='BARRA', max_length=1, blank=True, null=True)  # Field name made lowercase.
    outros = models.CharField(db_column='OUTROS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    diabetico = models.CharField(db_column='DIABETICO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hipertenso = models.CharField(db_column='HIPERTENSO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    hivpositivo = models.CharField(db_column='HIVPOSITIVO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    fumante = models.CharField(db_column='FUMANTE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    ativo = models.CharField(db_column='ATIVO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codativo = models.CharField(db_column='CODATIVO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='TIPO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    datacad = models.DateTimeField(db_column='DATACAD', blank=True, null=True)  # Field name made lowercase.
    origem = models.CharField(db_column='ORIGEM', max_length=1, blank=True, null=True)  # Field name made lowercase.
    natural = models.CharField(db_column='NATURAL', max_length=50, blank=True, null=True)  # Field name made lowercase.
    relig = models.CharField(db_column='RELIG', max_length=20, blank=True, null=True)  # Field name made lowercase.
    cor = models.CharField(db_column='COR', max_length=20, blank=True, null=True)  # Field name made lowercase.
    grau = models.CharField(db_column='GRAU', max_length=20, blank=True, null=True)  # Field name made lowercase.
    supcorp = models.FloatField(db_column='SUPCORP', blank=True, null=True)  # Field name made lowercase.
    dc = models.FloatField(db_column='DC', blank=True, null=True)  # Field name made lowercase.
    grupoemp = models.CharField(db_column='GRUPOEMP', max_length=2)  # Field name made lowercase.
    filial = models.CharField(db_column='FILIAL', max_length=2)  # Field name made lowercase.
    cli_codigo_ex = models.CharField(db_column='CLI_CODIGO_EX', max_length=10, blank=True, null=True)  # Field name made lowercase.
    obsficha = models.CharField(db_column='OBSFICHA', max_length=500, blank=True, null=True)  # Field name made lowercase.
    cns = models.CharField(db_column='CNS', max_length=20, blank=True, null=True)  # Field name made lowercase.
    obito = models.CharField(db_column='OBITO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    locorigem = models.CharField(db_column='LOCORIGEM', max_length=15, blank=True, null=True)  # Field name made lowercase.
    chave_sline = models.CharField(db_column='CHAVE_SLINE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    envia_medico = models.CharField(db_column='ENVIA_MEDICO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    plano2 = models.CharField(db_column='PLANO2', max_length=30, blank=True, null=True)  # Field name made lowercase.
    codexp = models.CharField(db_column='CODEXP', max_length=6, blank=True, null=True)  # Field name made lowercase.
    lograd = models.CharField(db_column='LOGRAD', max_length=30, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(max_length=50, blank=True, null=True)
    anoadesao = models.CharField(db_column='ANOADESAO', max_length=5, blank=True, null=True)  # Field name made lowercase.
    corraca = models.CharField(db_column='CORRACA', max_length=2, blank=True, null=True)  # Field name made lowercase.
    grauinstrucao = models.CharField(db_column='GRAUINSTRUCAO', max_length=2, blank=True, null=True)  # Field name made lowercase.
    celular = models.CharField(db_column='CELULAR', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codmae = models.CharField(db_column='CODMAE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    alergia = models.CharField(db_column='ALERGIA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    obsalergia = models.CharField(db_column='OBSALERGIA', max_length=50, blank=True, null=True)  # Field name made lowercase.
    usubloq = models.CharField(db_column='USUBLOQ', max_length=15, blank=True, null=True)  # Field name made lowercase.
    databloq = models.DateTimeField(db_column='DATABLOQ', blank=True, null=True)  # Field name made lowercase.
    telefone2 = models.CharField(db_column='TELEFONE2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    complemento = models.CharField(db_column='COMPLEMENTO', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tituloeleitor = models.CharField(db_column='TITULOELEITOR', max_length=30, blank=True, null=True)  # Field name made lowercase.
    uftituloeleitor = models.CharField(db_column='UFTITULOELEITOR', max_length=2, blank=True, null=True)  # Field name made lowercase.
    gruposangue = models.CharField(max_length=3, blank=True, null=True)
    etnia = models.CharField(db_column='ETNIA', max_length=4, blank=True, null=True)  # Field name made lowercase.
    resgate = models.DateTimeField(db_column='RESGATE', blank=True, null=True)  # Field name made lowercase.
    parentesco = models.CharField(db_column='PARENTESCO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    setor = models.CharField(db_column='SETOR', max_length=50, blank=True, null=True)  # Field name made lowercase.
    dataadm = models.DateTimeField(db_column='DATAADM', blank=True, null=True)  # Field name made lowercase.
    id_pac_oracle = models.CharField(db_column='ID_PAC_ORACLE', max_length=15, blank=True, null=True)  # Field name made lowercase.
    codproduto = models.CharField(db_column='CODPRODUTO', max_length=10, blank=True, null=True)  # Field name made lowercase.
    historiamedicapregressa = models.TextField(db_column='HistoriaMedicaPregressa', blank=True, null=True)  # Field name made lowercase.
    outrasalergias = models.TextField(db_column='OUTRASALERGIAS', blank=True, null=True)  # Field name made lowercase.
    abrev = models.CharField(db_column='ABREV', max_length=12, blank=True, null=True)  # Field name made lowercase.
    antecedenteclinico = models.TextField(db_column='AntecedenteClinico', blank=True, null=True)  # Field name made lowercase.
    antecedentefamiliar = models.TextField(db_column='AntecedenteFamiliar', blank=True, null=True)  # Field name made lowercase.
    nomesocial = models.CharField(db_column='NOMESOCIAL', max_length=100, blank=True, null=True)  # Field name made lowercase.
    obs58 = models.CharField(db_column='OBS58', max_length=100, blank=True, null=True)  # Field name made lowercase.
    renal = models.BooleanField(db_column='Renal', blank=True, null=True)  # Field name made lowercase.
    cbo = models.CharField(db_column='CBO', max_length=20, blank=True, null=True)  # Field name made lowercase.
    migracao = models.BooleanField(db_column='MIGRACAO', blank=True, null=True)  # Field name made lowercase.
    codrespcorrente = models.CharField(db_column='CODRESPCORRENTE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    whatsapp = models.CharField(db_column='WhatsApp', max_length=11, blank=True, null=True)  # Field name made lowercase.
    nguiaenc = models.CharField(db_column='NGUIAENC', max_length=10, blank=True, null=True)  # Field name made lowercase.
    codfidelidade = models.CharField(db_column='CODFIDELIDADE', max_length=12, blank=True, null=True)  # Field name made lowercase.
    estrangeiro = models.CharField(db_column='ESTRANGEIRO', max_length=1, blank=True, null=True)  # Field name made lowercase.
    codpais = models.CharField(db_column='CODPAIS', max_length=5, blank=True, null=True)  # Field name made lowercase.
    codencaminha = models.CharField(db_column='CODENCAMINHA', max_length=5, blank=True, null=True)  # Field name made lowercase.
    habitovida = models.TextField(db_column='HabitoVida', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CADPACIENTE'
        unique_together = (('codpaciente', 'paciente', 'sexo', 'datanasc', 'naturalidade', 'cpf', 'endereco', 'bairro', 'cidade', 'estado', 'datasist', 'codconvenio', 'profissao', 'idade', 'rg', 'oe', 'cep', 'telefone', 'matricula', 'titular', 'resp', 'end_resp', 'plano', 'quant', 'ult_vez', 'usuario', 'ec', 'validade', 'ultpagto', 'md', 'mesnasc', 'peso', 'altura', 'datanascr', 'medico', 'nome', 'filiacao', 'tipodoc', 'codmun', 'codmed', 'numero', 'telresp', 'barra', 'outros', 'diabetico', 'hipertenso', 'hivpositivo', 'fumante', 'ativo', 'codativo', 'tipo', 'datacad', 'origem', 'natural', 'relig', 'cor', 'grau', 'supcorp', 'dc', 'grupoemp', 'filial', 'cli_codigo_ex', 'obsficha', 'cns', 'obito', 'locorigem', 'chave_sline', 'envia_medico', 'plano2', 'codexp', 'lograd', 'email', 'anoadesao', 'corraca', 'grauinstrucao'),)

    def __str__(self):
        return self.paciente


class Entrada(models.Model):
    codmovimento = models.CharField(db_column='CodMovimento', primary_key=True, max_length=10)  # Field name made lowercase.
    codpaciente = models.ForeignKey(Cadpaciente, db_column='CodPaciente', max_length=7, on_delete=models.PROTECT)  # Field name made lowercase.
    codconvenio = models.CharField(db_column='CodConvenio', max_length=10)  # Field name made lowercase.
    matricula = models.CharField(db_column='Matricula', max_length=30, blank=True,
                                 null=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=10)  # Field name made lowercase.
    datahoraent = models.DateTimeField(db_column='DataHoraEnt')  # Field name made lowercase.
    datahorasai = models.DateTimeField(db_column='DataHoraSai', blank=True, null=True)  # Field name made lowercase.
    datahorautient = models.DateTimeField(db_column='DataHoraUtiEnt', blank=True,
                                          null=True)  # Field name made lowercase.
    datahorautisai = models.DateTimeField(db_column='DataHoraUtiSai', blank=True,
                                          null=True)  # Field name made lowercase.
    guia = models.CharField(db_column='Guia', max_length=100, blank=True, null=True)  # Field name made lowercase.
    prontuario = models.CharField(db_column='Prontuario', max_length=25, blank=True,
                                  null=True)  # Field name made lowercase.
    hist = models.CharField(db_column='Hist', max_length=150, blank=True, null=True)  # Field name made lowercase.
    codmedico = models.CharField(db_column='CodMedico', max_length=5)  # Field name made lowercase.
    codanest = models.CharField(db_column='CodAnest', max_length=5, blank=True,
                                null=True)  # Field name made lowercase.
    codprim = models.CharField(db_column='CodPrim', max_length=5, blank=True,
                               null=True)  # Field name made lowercase.
    codseg = models.CharField(db_column='CodSeg', max_length=5, blank=True, null=True)  # Field name made lowercase.
    codinstrum = models.CharField(db_column='CodInstrum', max_length=6, blank=True,
                                  null=True)  # Field name made lowercase.
    taxaacomod = models.CharField(db_column='Taxaacomod', max_length=8, blank=True,
                                  null=True)  # Field name made lowercase.
    local = models.CharField(db_column='Local', max_length=20)  # Field name made lowercase.
    acomod = models.CharField(db_column='Acomod', max_length=50, blank=True,
                              null=True)  # Field name made lowercase.
    recep = models.CharField(db_column='Recep', max_length=10, blank=True, null=True)  # Field name made lowercase.
    total = models.FloatField(db_column='Total', blank=True, null=True)  # Field name made lowercase.
    fechado = models.CharField(db_column='Fechado', max_length=1)  # Field name made lowercase.
    nfech = models.CharField(db_column='NFech', max_length=10, blank=True, null=True)  # Field name made lowercase.
    enviado = models.CharField(db_column='Enviado', max_length=1, blank=True,
                               null=True)  # Field name made lowercase.
    codamb = models.CharField(db_column='CodAmb', max_length=10, blank=True,
                              null=True)  # Field name made lowercase.
    codamb2 = models.CharField(db_column='CodAmb2', max_length=10, blank=True,
                               null=True)  # Field name made lowercase.
    codcid = models.CharField(db_column='CodCid', max_length=11, blank=True,
                              null=True)  # Field name made lowercase.
    horacir = models.DateTimeField(db_column='HoraCir', blank=True, null=True)  # Field name made lowercase.
    consultaok = models.CharField(db_column='Consultaok', max_length=15, blank=True,
                                  null=True)  # Field name made lowercase.
    restrito = models.CharField(db_column='Restrito', max_length=1, blank=True,
                                null=True)  # Field name made lowercase.
    motivo = models.CharField(db_column='Motivo', max_length=100, blank=True,
                              null=True)  # Field name made lowercase.
    obito = models.CharField(db_column='Obito', max_length=5, blank=True, null=True)  # Field name made lowercase.
    deposito = models.FloatField(db_column='Deposito', blank=True, null=True)  # Field name made lowercase.
    dataentrega = models.DateTimeField(db_column='DataEntrega', blank=True, null=True)  # Field name made lowercase.
    codsolic = models.CharField(db_column='CodSolic', max_length=6, blank=True,
                                null=True)  # Field name made lowercase.
    medsolic = models.CharField(db_column='Medsolic', max_length=60, blank=True,
                                null=True)  # Field name made lowercase.
    usuario = models.CharField(db_column='Usuario', max_length=30, blank=True,
                               null=True)  # Field name made lowercase.
    datasist = models.DateTimeField(db_column='DataSist', blank=True, null=True)  # Field name made lowercase.
    datahoraagd = models.CharField(db_column='DataHoraAgd', max_length=50, blank=True,
                                   null=True)  # Field name made lowercase.
    interno = models.CharField(db_column='Interno', max_length=20, blank=True,
                               null=True)  # Field name made lowercase.
    mes = models.IntegerField(db_column='Mes', blank=True, null=True)  # Field name made lowercase.
    ano = models.IntegerField(db_column='Ano', blank=True, null=True)  # Field name made lowercase.
    pacote = models.CharField(db_column='Pacote', max_length=3, blank=True, null=True)  # Field name made lowercase.
    nd = models.IntegerField(db_column='ND', blank=True, null=True)  # Field name made lowercase.
    codped = models.CharField(db_column='CodPed', max_length=5, blank=True, null=True)  # Field name made lowercase.
    datanascr = models.DateTimeField(db_column='DataNascr', blank=True, null=True)  # Field name made lowercase.
    senha = models.CharField(db_column='Senha', max_length=100, blank=True, null=True)  # Field name made lowercase.
    quant = models.IntegerField(db_column='Quant', blank=True, null=True)  # Field name made lowercase.
    entrega = models.CharField(db_column='Entrega', max_length=30, blank=True,
                               null=True)  # Field name made lowercase.
    eletiva = models.CharField(db_column='Eletiva', max_length=1, blank=True,
                               null=True)  # Field name made lowercase.
    codant = models.CharField(db_column='CodAnt', max_length=100, blank=True,
                              null=True)  # Field name made lowercase.
    recebido = models.CharField(db_column='Recebido', max_length=1, blank=True,
                                null=True)  # Field name made lowercase.
    obs = models.CharField(db_column='Obs', max_length=200, blank=True, null=True)  # Field name made lowercase.
    topo = models.CharField(db_column='Topo', max_length=10, blank=True, null=True)  # Field name made lowercase.
    morfo = models.CharField(db_column='Morfo', max_length=50, blank=True, null=True)  # Field name made lowercase.
    cidm = models.CharField(db_column='Cidm', max_length=10, blank=True, null=True)  # Field name made lowercase.
    rn = models.CharField(db_column='RN', max_length=25, blank=True, null=True)  # Field name made lowercase.
    mc = models.CharField(db_column='MC', max_length=3, blank=True, null=True)  # Field name made lowercase.
    ident = models.CharField(db_column='Ident', max_length=1, blank=True, null=True)  # Field name made lowercase.
    contauso = models.CharField(db_column='ContaUso', max_length=1, blank=True,
                                null=True)  # Field name made lowercase.
    recup = models.CharField(db_column='Recup', max_length=1, blank=True, null=True)  # Field name made lowercase.
    origem = models.CharField(db_column='Origem', max_length=10, blank=True,
                              null=True)  # Field name made lowercase.
    alta = models.DateTimeField(db_column='Alta', blank=True, null=True)  # Field name made lowercase.
    obs2 = models.CharField(db_column='Obs2', max_length=150, blank=True, null=True)  # Field name made lowercase.
    acomodc = models.CharField(db_column='AcomodC', max_length=50, blank=True,
                               null=True)  # Field name made lowercase.
    ih = models.CharField(db_column='IH', max_length=30, blank=True, null=True)  # Field name made lowercase.
    crm = models.CharField(db_column='CRM', max_length=10, blank=True, null=True)  # Field name made lowercase.
    consolid = models.CharField(db_column='Consolid', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    nfiscal = models.CharField(db_column='NFiscal', max_length=10, blank=True,
                               null=True)  # Field name made lowercase.
    serie = models.CharField(db_column='Serie', max_length=10, blank=True, null=True)  # Field name made lowercase.
    medobito = models.CharField(db_column='MedObito', max_length=5, blank=True,
                                null=True)  # Field name made lowercase.
    npedlab = models.IntegerField(db_column='Npedlab', blank=True, null=True)  # Field name made lowercase.
    locorigem = models.CharField(db_column='LocOrigem', max_length=10, blank=True,
                                 null=True)  # Field name made lowercase.
    plano = models.CharField(db_column='Plano', max_length=50)  # Field name made lowercase.
    nfechr = models.CharField(db_column='Nfechr', max_length=7, blank=True, null=True)  # Field name made lowercase.
    glosa = models.FloatField(db_column='Glosa', blank=True, null=True)  # Field name made lowercase.
    nfechrc = models.CharField(db_column='Nfechrc', max_length=10, blank=True,
                               null=True)  # Field name made lowercase.
    codaux = models.CharField(db_column='CodaUX', max_length=15, blank=True,
                              null=True)  # Field name made lowercase.
    tabserv = models.CharField(db_column='Tabserv', max_length=10, blank=True,
                               null=True)  # Field name made lowercase.
    tabhm = models.CharField(db_column='Tabhm', max_length=10, blank=True, null=True)  # Field name made lowercase.
    numrestr = models.IntegerField(db_column='Numrestr', blank=True, null=True)  # Field name made lowercase.
    dataref = models.DateTimeField(db_column='DataRef', blank=True, null=True)  # Field name made lowercase.
    grupoemp = models.CharField(db_column='GrupoEmp', max_length=2)  # Field name made lowercase.
    filial = models.CharField(db_column='Filial', max_length=2)  # Field name made lowercase.
    datafech = models.DateTimeField(db_column='DataFech', blank=True, null=True)  # Field name made lowercase.
    codsus = models.CharField(db_column='CodSus', max_length=10, blank=True,
                              null=True)  # Field name made lowercase.
    entemerg = models.CharField(db_column='EntEmerg', max_length=2, blank=True,
                                null=True)  # Field name made lowercase.
    ordem = models.CharField(db_column='Ordem', max_length=5, blank=True, null=True)  # Field name made lowercase.
    prefere = models.CharField(db_column='Prefere', max_length=15, blank=True,
                               null=True)  # Field name made lowercase.
    motsaitiss = models.CharField(db_column='Motsaitiss', max_length=5, blank=True,
                                  null=True)  # Field name made lowercase.
    regobt = models.CharField(db_column='Regobt', max_length=10, blank=True,
                              null=True)  # Field name made lowercase.
    cidobito = models.CharField(db_column='CidObito', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    obitof = models.CharField(db_column='Obitof', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tipoint = models.CharField(db_column='TipoInt', max_length=1, blank=True,
                               null=True)  # Field name made lowercase.
    tipoatend = models.CharField(db_column='TipoAtend', max_length=2, blank=True,
                                 null=True)  # Field name made lowercase.
    tiposaida = models.CharField(db_column='Tiposaida', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    tipoconsulta = models.CharField(db_column='Tipoconsulta', max_length=1, blank=True,
                                    null=True)  # Field name made lowercase.
    guiaprincipal = models.CharField(db_column='GuiaPrincipal', max_length=30, blank=True,
                                     null=True)  # Field name made lowercase.
    peso = models.FloatField(db_column='Peso', blank=True, null=True)  # Field name made lowercase.
    altura = models.FloatField(db_column='Altura', blank=True, null=True)  # Field name made lowercase.
    condguia = models.CharField(db_column='CondGuia', max_length=1, blank=True,
                                null=True)  # Field name made lowercase.
    graumedicoent = models.CharField(db_column='Graumedicoent', max_length=2, blank=True,
                                     null=True)  # Field name made lowercase.
    codexp = models.CharField(db_column='CodExp', max_length=12, blank=True,
                              null=True)  # Field name made lowercase.
    nlote = models.IntegerField(db_column='NLote', blank=True, null=True)  # Field name made lowercase.
    dataautsenha = models.DateTimeField(db_column='DataAutsenha', blank=True,
                                        null=True)  # Field name made lowercase.
    datavalsenha = models.DateTimeField(db_column='DataValsenha', blank=True,
                                        null=True)  # Field name made lowercase.
    indicacid = models.CharField(db_column='IndicAcid', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    tipodoenca = models.CharField(db_column='Tipodoenca', max_length=1, blank=True,
                                  null=True)  # Field name made lowercase.
    tempodoenca = models.CharField(db_column='Tempodoenca', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    quanttempo = models.IntegerField(db_column='Quanttempo', blank=True, null=True)  # Field name made lowercase.
    quantdoenca = models.IntegerField(db_column='Quantdoenca', blank=True, null=True)  # Field name made lowercase.
    parcial = models.CharField(db_column='Parcial', max_length=1, blank=True,
                               null=True)  # Field name made lowercase.
    dataentcon = models.DateTimeField(db_column='DataEntcon', blank=True, null=True)  # Field name made lowercase.
    triagem = models.CharField(db_column='Triagem', max_length=1, blank=True,
                               null=True)  # Field name made lowercase.
    datamedic = models.DateTimeField(db_column='DataMedic', blank=True, null=True)  # Field name made lowercase.
    datatriagem = models.DateTimeField(db_column='DataTriagem', blank=True, null=True)  # Field name made lowercase.
    dataconsulta = models.DateTimeField(db_column='DataConsulta', blank=True,
                                        null=True)  # Field name made lowercase.
    codvermelho = models.CharField(db_column='CodVermelho', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    tipotiss = models.CharField(db_column='TipoTiss', max_length=1, blank=True,
                                null=True)  # Field name made lowercase.
    fungulin = models.IntegerField(db_column='Fungulin', blank=True, null=True)  # Field name made lowercase.
    tiss28 = models.CharField(db_column='Tiss28', max_length=5, blank=True, null=True)  # Field name made lowercase.
    ndoccir = models.CharField(db_column='NDocCir', max_length=10, blank=True,
                               null=True)  # Field name made lowercase.
    datasolic = models.DateTimeField(db_column='DataSolic', blank=True, null=True)  # Field name made lowercase.
    datapreexame = models.DateTimeField(db_column='DataPreexame', blank=True,
                                        null=True)  # Field name made lowercase.
    chklistpqa = models.CharField(db_column='ChkListpqa', max_length=10, blank=True,
                                  null=True)  # Field name made lowercase.
    datahoraint = models.DateTimeField(db_column='DataHoraInt', blank=True, null=True)  # Field name made lowercase.
    prevalta = models.DateTimeField(db_column='Prevalta', blank=True, null=True)  # Field name made lowercase.
    loteent = models.CharField(db_column='LoteEnt', max_length=10, blank=True,
                               null=True)  # Field name made lowercase.
    codmae = models.CharField(db_column='CodMae', max_length=10, blank=True,
                              null=True)  # Field name made lowercase.
    datahoraobs = models.DateTimeField(db_column='DataHoraObs', blank=True, null=True)  # Field name made lowercase.
    motivoatd = models.CharField(db_column='Motivoatd', max_length=100, blank=True,
                                 null=True)  # Field name made lowercase.
    previsaoentrega = models.DateTimeField(db_column='Previsaoentrega', blank=True,
                                           null=True)  # Field name made lowercase.
    codtus = models.CharField(db_column='CodTus', max_length=8, blank=True, null=True)  # Field name made lowercase.
    alertasirs = models.CharField(db_column='AlertaSirs', max_length=20, blank=True,
                                  null=True)  # Field name made lowercase.
    valcota = models.FloatField(db_column='Valcota', blank=True, null=True)  # Field name made lowercase.
    localini = models.CharField(db_column='Localini', max_length=15, blank=True,
                                null=True)  # Field name made lowercase.
    importbpa = models.CharField(db_column='Importbpa', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    natendimento = models.IntegerField(db_column='Natendimento', blank=True,
                                       null=True)  # Field name made lowercase.
    senhaweb = models.CharField(db_column='Senhaweb', max_length=10, blank=True,
                                null=True)  # Field name made lowercase.
    auditado = models.CharField(db_column='Auditado', max_length=1, blank=True,
                                null=True)  # Field name made lowercase.
    datamarcada = models.DateTimeField(db_column='DataMarcada', blank=True, null=True)  # Field name made lowercase.
    parentesco = models.CharField(db_column='Parentesco', max_length=20, blank=True,
                                  null=True)  # Field name made lowercase.
    bloquearconta = models.BooleanField(db_column='Bloquearconta', blank=True,
                                        null=True)  # Field name made lowercase.
    tipoatend2 = models.CharField(db_column='Tipoatend2', max_length=2, blank=True,
                                  null=True)  # Field name made lowercase.
    guiaoper = models.CharField(db_column='GuiaOper', max_length=30, blank=True,
                                null=True)  # Field name made lowercase.
    dataentexa = models.DateTimeField(db_column='DataEntexa', blank=True, null=True)  # Field name made lowercase.
    totalsimu = models.FloatField(db_column='Totalsimu', blank=True, null=True)  # Field name made lowercase.
    totparceiro = models.FloatField(db_column='Totparceiro', blank=True, null=True)  # Field name made lowercase.
    codespec = models.CharField(db_column='CodEspec', max_length=20, blank=True,
                                null=True)  # Field name made lowercase.
    fechadocred = models.CharField(db_column='FechadoCred', max_length=1, blank=True,
                                   null=True)  # Field name made lowercase.
    nfechcred = models.CharField(db_column='NFechCred', max_length=6, blank=True,
                                 null=True)  # Field name made lowercase.
    totalcred = models.FloatField(db_column='Totalcred', blank=True, null=True)  # Field name made lowercase.
    idsenhaatd = models.IntegerField(db_column='IDSenhaATD', blank=True, null=True)  # Field name made lowercase.
    ndocextra = models.IntegerField(db_column='Ndocextra', blank=True, null=True)  # Field name made lowercase.
    senhalaudoweb = models.CharField(db_column='Senhalaudoweb', max_length=20, blank=True,
                                     null=True)  # Field name made lowercase.
    grupoproc = models.CharField(db_column='GrupoProc', max_length=5, blank=True,
                                 null=True)  # Field name made lowercase.
    cbosus = models.CharField(db_column='CBOSus', max_length=6, blank=True, null=True)  # Field name made lowercase.
    encaixe = models.CharField(db_column='Encaixe', max_length=1, blank=True,
                               null=True)  # Field name made lowercase.
    datarecalc = models.DateTimeField(db_column='DataRecalc', blank=True, null=True)  # Field name made lowercase.
    avaliacaoatendimentoenviada = models.BooleanField(db_column='AvaliacaoAtendimentoEnviada', blank=True,
                                                      null=True)  # Field name made lowercase.
    parecer = models.CharField(db_column='PARECER', max_length=1, blank=True,
                               null=True)  # Field name made lowercase.
    regimeint = models.CharField(db_column='REGIMEINT', max_length=1, blank=True,
                                 null=True)  # Field name made lowercase.
    emporigem = models.CharField(db_column='EMPORIGEM', max_length=2, blank=True,
                                 null=True)  # Field name made lowercase.
    fatura = models.FloatField(db_column='FATURA', blank=True, null=True)  # Field name made lowercase.
    prescrito = models.BooleanField(db_column='Prescrito', blank=True, null=True)  # Field name made lowercase.
    idimportcfi = models.CharField(db_column='idImportCFI', max_length=100, blank=True,
                                    null=True)  # Field name made lowercase.
    datadilatado = models.DateTimeField(db_column='DataDilatado', blank=True,
                                        null=True)  # Field name made lowercase.
    datadilatando = models.DateTimeField(db_column='DataDilatando', blank=True,
                                         null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Entrada'

    def __str__(self):
        return self.codmovimento


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
    codmovimento = models.CharField(primary_key=True, db_column='CodMovimento', max_length=10)  # Field name made lowercase.
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
        