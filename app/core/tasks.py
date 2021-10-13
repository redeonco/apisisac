from celery import shared_task
from mosaiq_app.models import *
from core.models import Agenda, Cadpaciente, Entrada, Entradaradio, Planejfisico, Radioterapia
from datetime import date


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def atualizaagenda():
    def addcodmovimento(codmovimento):
        cut = codmovimento.split('.')
        seqadd = int(cut[1]) + 1
        if seqadd < 10:
            seqadd = '0' + str(seqadd)
        codfinal = cut[0] + '.' + str(seqadd)  

        return codfinal
    
    query_mosaiq = Schedule.objects.filter(dataagenda__year=date.today().year, dataagenda__month=date.today().month, dataagenda__day=date.today().day).filter(status=' C')

    for obj in query_mosaiq.iterator():
        nome_paciente = str(obj.id_paciente.firstname) + ' ' + str(obj.id_paciente.lastname)
        dataagenda_mosaiq = obj.dataagenda

        codpac_sisac = Cadpaciente.objects.filter(paciente__contains=nome_paciente).filter(datanasc=obj.id_paciente.datanasc).first()
        if codpac_sisac is not None:            
            ultimo_codmov = Entrada.objects.filter(codpaciente=codpac_sisac.pk).order_by('datahoraent').last()
            novo_codmov = addcodmovimento(str(ultimo_codmov))

            agenda_sisac = Agenda.objects.filter(codpaciente=codpac_sisac).filter(datahora=dataagenda_mosaiq).first()
            if agenda_sisac is not None:

                entrada = Entrada()
                entrada.codpaciente = codpac_sisac.pk
                entrada.codmovimento = novo_codmov
                entrada.tipo = '4'
                entrada.fechado = 'E'
                entrada.datahoraent = dataagenda_mosaiq
                entrada.local = ''
                entrada.usuario = 'API'
                entrada.codconvenio = ultimo_codmov.codconvenio
                entrada.plano = ''
                entrada.codmedico = ultimo_codmov.codmedico
                entrada.hist = 'Sessão de Radioterapia'
                entrada.total = 0
                entrada.grupoemp = '01'
                entrada.filial = '01'
                entrada.save()

                prescricao = Radioterapia.objects.filter(codpaciente=codpac_sisac.pk).order_by('numpresc').last()
                planejamento = Planejfisico.objects.filter(numpresc=prescricao.pk).order_by('idplanejfisico').first()

                entradaradio = Entradaradio()
                entradaradio.codmovimento = novo_codmov
                entradaradio.codpaciente = codpac_sisac.pk
                entradaradio.numpresc = prescricao
                entradaradio.idplanejfisico = planejamento.pk
                entradaradio.encerrado = 'S'
                entradaradio.observacao = ''
                entradaradio.usuario = 'API'
                entradaradio.datahora = dataagenda_mosaiq
                entradaradio.datasist = dataagenda_mosaiq
                entradaradio.nplanejamento = planejamento.nplanejamento
                entradaradio.nomecampo = planejamento.nomecampo
                entradaradio.incidencia = planejamento.incidencia
                entradaradio.ntratamento = planejamento.ntratamento
                entradaradio.ncampo = planejamento.ncampo
                entradaradio.grupoemp = '01'
                entradaradio.filial = '01'
                entradaradio.save()

                agenda_sisac.confatd = 'S'
                agenda_sisac.usuario = 'API'
                agenda_sisac.codmovimento = novo_codmov
                agenda_sisac.save()

