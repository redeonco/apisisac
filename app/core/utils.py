from core.functions import incrementa_codigoexame, incrementa_natendimento
from core.models import Entrada, Exame, Fatura
from core.resources.classes import TreatmentConstructor
from core.resources.constants import API_USER


def lanca_pacote_tratamento(cod_paciente: int):
    TreatmentConstructor(cod_paciente)

    TREATMENT_DATA = TreatmentConstructor.construct_initial_data()

    if not TREATMENT_DATA:
        print('Nenhum dado de tratamento disponível... Retornando False.')
        return False

    print(f'Dados de tratamento processados para paciente {TREATMENT_DATA.paciente.paciente}.')
    print('Iniciando verificação de elegibilidade para lançar tratamento.')
    is_there_entrada_tratamento = Entrada.objects\
        .filter(codpaciente=cod_paciente)\
        .filter(codamb=TREATMENT_DATA.codamb)\
        .count() == 0

    is_there_fatura_tratamento = Fatura.objects\
        .filter(codpaciente__icontains=cod_paciente.codpaciente)\
        .filter(codamb=TREATMENT_DATA.codamb)\
        .count() == 0

    is_there_exame_tratamento = Exame.objects\
        .filter(codpaciente__icontains=cod_paciente.codpaciente)\
        .filter(codamb=TREATMENT_DATA.codamb)\
        .count() == 0

    if is_there_entrada_tratamento:
        entrada = Entrada(
            codmovimento=TREATMENT_DATA.novo_codmov,
            codpaciente=cod_paciente,
            codconvenio=TREATMENT_DATA.convenio.codconvenio,
            matricula=TREATMENT_DATA.matricula,
            tipo='4',
            datahoraent=TREATMENT_DATA.data_referencia,
            hist=TREATMENT_DATA.procedimento.descr,
            codmedico=TREATMENT_DATA.codmedico,
            local='112',
            recep=API_USER,
            total=TREATMENT_DATA.procedimento.ch,
            fechado='P',
            codamb=TREATMENT_DATA.codamb,
            datasist=TREATMENT_DATA.data_referencia,
            plano=TREATMENT_DATA.plano,
            tabhm=TREATMENT_DATA.convenio.hm,
            datahoraint=TREATMENT_DATA.data_referencia,
            localini='112',
            natendimento=incrementa_natendimento(),
            datamarcada=TREATMENT_DATA.data_referencia,
        )
        entrada.save()
        print('Registro na tabela Entrada gravado com sucesso.')

    if is_there_fatura_tratamento:
        fatura = Fatura(
            codpaciente=TREATMENT_DATA.novo_codmov,
            grupo='1',
            codtaxa=TREATMENT_DATA.codamb,
            descr=TREATMENT_DATA.procedimento.descr,
            data=TREATMENT_DATA.TREATMENT_DATA.data_referencia,
            valor=TREATMENT_DATA.procedimento.ch,
            quant='1',
            filme='0',
            codmedico=TREATMENT_DATA.codmedico,
            datasist=TREATMENT_DATA.data_referencia,
            usuario=API_USER,
            codamb=TREATMENT_DATA.codamb,
            ch=TREATMENT_DATA.procedimento.ch,
            local='112',
            honor=TREATMENT_DATA.procedimento.ch,
            vpprof=TREATMENT_DATA.procedimento.ch,
            obs=f'Tab.Honor {TREATMENT_DATA.convenio.hm} {TREATMENT_DATA.convenio.descr}',
            localac='112',
        )
        fatura.save()
        print('Registro na tabela Fatura gravado com sucesso.')

    if is_there_exame_tratamento:
        exame = Exame(
            codpaciente=TREATMENT_DATA.novo_codmov,
            codamb=TREATMENT_DATA.codamb,
            local='112',
            descr=TREATMENT_DATA.procedimento.descr,
            quant='1',
            codmedico=TREATMENT_DATA.codmedico,
            usuario=API_USER,
            datasist=TREATMENT_DATA.data_referencia,
            chave=TREATMENT_DATA.novo_codmov,
            valor=TREATMENT_DATA.procedimento.ch,
            tipo='R',
            dataproc=TREATMENT_DATA.data_referencia,
            codpacref=cod_paciente,
            codigo=incrementa_codigoexame(),
        )
        exame.save()
        print('Registro na tabela Exame gravado com sucesso.')
    
    print(f'Finalizado lançamento do tratamento para paciente {TREATMENT_DATA.paciente.paciente}\n')

def lanca_pacote_em_massa(lista_pacientes: list) -> None:
    for paciente in lista_pacientes:
        lanca_pacote_tratamento(paciente)
