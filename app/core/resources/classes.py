from datetime import datetime
from app.core.functions import addcodmovimento
from app.core.models import Agenda, CadConvenio, Cadpaciente, Entrada, Radioterapia, SolicExa, TabAmb


class Treatment:
    def __init__(
        self, 
        paciente: Cadpaciente, 
        prescricao: Radioterapia, 
        solicitacao_tratamento: SolicExa, 
        primeira_entrada: Entrada, 
        ultima_entrada: Entrada, 
        convenio: CadConvenio,
        novo_codmov: str
    ) -> None:
        self.paciente = paciente
        self.prescricao = prescricao
        self.solicitacao_tratamento = solicitacao_tratamento
        self.primeira_entrada = primeira_entrada
        self.ultima_entrada = ultima_entrada
        self.convenio = convenio
        self.codamb = self.solicitacao_tratamento.codamb
        self.codmedico = self.solicitacao_tratamento.codmedico
        self.matricula = self.primeira_entrada.matricula
        self.plano = self.primeira_entrada.plano
        self.novo_codmov = novo_codmov
        print('Instanciando objeto Treatment...')
    
    @property
    def procedimento(self):
        return TabAmb.objects.filter(codamb=self.codamb).filter(codconvenio=self.convenio.hm).first()

    @property
    def data_referencia(self):
        ref_date = Agenda.objects\
            .filter(tipo='RAD')\
            .filter(confatd='S')\
            .filter(codpaciente=self.paciente.codpaciente)\
            .order_by('IDAgenda').first()

        return ref_date.datahora if ref_date else datetime.now()

class TreatmentConstructor:
    def __init__(self, cod_paciente: int) -> None:
        self.cod_paciente = cod_paciente
    
    def construct_initial_data(self) -> Treatment:
        print('\nIniciando constructor de dados iniciais para o tratamento.')
        paciente = Cadpaciente.objects.get(pk=self.cod_paciente)
        if not paciente:
            print('Paciente não encontrado. Retornando False...')
            return False

        prescricao = Radioterapia.objects.filter(codpaciente=paciente).order_by('numpresc').last()

        if prescricao:
            solicitacao_tratamento = SolicExa.objects\
                .filter(npresc=prescricao.numpresc)\
                .order_by('item')\
                .first()

            primeira_entrada = Entrada.objects\
                .filter(codmovimento=solicitacao_tratamento.codpaciente)\
                .first()

            ultima_entrada = Entrada.objects\
                .filter(codpaciente=paciente.codpaciente)\
                .filter(filial='01').order_by('datahoraent')\
                .last()
            
            convenio = CadConvenio.objects.get(codconvenio=solicitacao_tratamento.codconvenio)
        
        if primeira_entrada and ultima_entrada:
            novo_codmov = addcodmovimento(str(ultima_entrada.codmovimento))
            print(f'Construção finalizada. Retornando dados do tratamento para o paciente {paciente.paciente}')
            return Treatment(
                paciente, 
                prescricao, 
                solicitacao_tratamento, 
                primeira_entrada, 
                ultima_entrada, 
                convenio,
                novo_codmov
            )

        else:
            return False
