from celery import shared_task
from mosaiq_app.models import *
from core.models import Agenda, Cadpaciente, Entrada, Entradaradio, Planejfisico, Radioterapia
from datetime import datetime, date
from django.db.models import Q


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
    
    horainicial = datetime.now()

    print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Consultando agenda MOSAIQ...')
    query_mosaiq = Schedule.objects.filter(dataagenda__year=date.today().year, dataagenda__month=date.today().month, dataagenda__day='13').filter(status=' C')
    print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Consulta concluída com sucesso.')

    print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Iniciando iteração no resultado da consulta...')
    i = 0
    for obj in query_mosaiq.iterator():
        print('---------------------------------------------')
        cpf_paciente = obj.id_paciente.cpf
        dataagenda_mosaiq = obj.dataagenda

        codpac_sisac = Cadpaciente.objects.filter(cpf=cpf_paciente).first()
        if codpac_sisac is not None:     
            print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Iniciando execuções para o paciente', codpac_sisac)       
            ultimo_codmov = Entrada.objects.filter(codpaciente=codpac_sisac.pk).order_by('datahoraent').last()
            novo_codmov = addcodmovimento(str(ultimo_codmov))

            agenda_sisac = Agenda.objects.filter(codpaciente=codpac_sisac).filter(datahora=dataagenda_mosaiq).first()
            if agenda_sisac is not None:
                print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Gerando registro na tabela entrada...')
                entrada = Entrada()
                entrada.codpaciente = codpac_sisac.pk
                entrada.codmovimento = novo_codmov
                entrada.tipo = '4'
                entrada.fechado = 'E'
                entrada.datahoraent = dataagenda_mosaiq
                entrada.datasist = datetime.now()
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
                print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Registro gerado na tabela entrada.')

                print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Buscando registros de prescrição e planejamento...')
                prescricao = Radioterapia.objects.filter(codpaciente=codpac_sisac.pk).order_by('numpresc').last()
                planejamento = Planejfisico.objects.filter(numpresc=prescricao.pk).order_by('idplanejfisico')

                print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Busca concluída.')
                print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Iniciando iteração no resultado da busca...')
                n = 0
                print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Gerando registros na tabela EntradaRadio...')
                for planej in planejamento.iterator():                    
                    entradaradio = Entradaradio()
                    entradaradio.codmovimento = novo_codmov
                    entradaradio.codpaciente = codpac_sisac.pk
                    entradaradio.numpresc = prescricao
                    entradaradio.idplanejfisico = planej.pk
                    entradaradio.encerrado = 'S'
                    entradaradio.observacao = ''
                    entradaradio.usuario = 'API'
                    entradaradio.datahora = dataagenda_mosaiq
                    entradaradio.datasist = datetime.now()
                    entradaradio.nplanejamento = planej.nplanejamento
                    entradaradio.nomecampo = planej.nomecampo
                    entradaradio.incidencia = planej.incidencia
                    entradaradio.ntratamento = planej.ntratamento
                    entradaradio.ncampo = planej.ncampo
                    entradaradio.grupoemp = '01'
                    entradaradio.filial = '01'
                    entradaradio.save()
                    n += 1
                print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', n, 'registro(s) gerado(s) na tabela EntradaRadio.')

                print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Confirmando paciente na tabela Agenda Radioterapia...')
                agenda_sisac.confatd = 'S'
                agenda_sisac.usuario = 'API'
                agenda_sisac.codmovimento = novo_codmov
                agenda_sisac.save()
                print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Paciente confirmado.')
                print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Iteração concluída para o paciente', codpac_sisac)
                
        i += 1
    print('---------------------------------------------')
    print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Atualização da agenda concluída com sucesso.', i, 'pacientes foram confirmados na agenda de tratamento de radioterapia SISAC.')

    horafinal = datetime.now()
    tempodecorrido = horafinal - horainicial
    print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Tempo total decorrido:', tempodecorrido)

    query_mosaiq2 = Schedule.objects.filter(dataagenda__year=date.today().year, dataagenda__month=date.today().month, dataagenda__day='13').filter(~Q(status=' C')).filter(~Q(suppressed='1'))

    list = []
    for obj in query_mosaiq2.iterator():
        cpf_paciente = obj.id_paciente.cpf
        codpac_sisac = Cadpaciente.objects.filter(cpf=cpf_paciente).first()
        list.append(codpac_sisac.paciente)

    
