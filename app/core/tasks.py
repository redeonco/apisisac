from celery import shared_task
from mosaiq_app.models import *
from core.models import Agenda, Cadpaciente, Entrada, Entradaradio, Planejfisico, Radioterapia, Planejfisicoc
from datetime import datetime, date
from django.db.models import Q
from django.core.mail import send_mail


@shared_task
def sendmail(qtdconfirmado, data):
    send_mail(
        'Núcleo de Sistemas - Relatório API - SISAC',
        'Núcleo de Sistemas - Relatório API - SISAC. \n Olá. Segue resumo da execução da tarefa Atualiza Agenda, em ' + data.strftime("%d/%m/%Y às %H:%M:%S") +
        '. \nQuantidade de pacientes confirmados na agenda do SISAC: ' + str(qtdconfirmado) + '.',
        'chamado@oncoradium.com.br',
        ['tony.carvalho@oncoradium.com.br'],
        fail_silently=False,
    )
@shared_task
def sendmail_lista(lista, qtdconfirmado, data):
    send_mail(
        'Núcleo de Sistemas - Relatório API - SISAC',
        'Núcleo de Sistemas - Relatório API - SISAC. \n Olá. Segue resumo da execução da tarefa Atualiza Agenda, em ' + data.strftime("%d/%m/%Y às %H:%M:%S") +
        '. \nQuantidade de pacientes confirmados na agenda do SISAC: ' + str(qtdconfirmado) + 
        '. \nPacientes não confirmados: ' + str(lista) + 
        '. \nVerificar se os pacientes realizaram tratamento na máquina.',
        'chamado@oncoradium.com.br',
        ['tony.carvalho@oncoradium.com.br'],
        fail_silently=False,
    )

@shared_task
def mailtest():
    send_mail(
        'Núcleo de Sistemas - Relatório API - SISAC',
        'Teste',
        'chamado@oncoradium.com.br',
        ['tony.carvalho@oncoradium.com.br'],
        fail_silently=False,
    )

# Tarefa para atualizar a agenda de tratamento da radioterapia do SISAC comparando com a agenda de tratamento do MOSAIQ
# A tarefa olha para a agenda do MOSAIQ quais pacientes estão marcados como Completed
# Para cada paciente marcado como Completed, a tarefa realiza iterações no banco de dados SISAC
# Gerando registros na tabela Entrada, EntradaRadio e Agenda
# Confirmando na agenda de radioterapia do SISAC os pacientes tratados no MOSAIQ
@shared_task
def atualizaagenda():
    # Função que realiza incremento da sequencial no código de movimento do paciente.
    # Código de movimento é o registro de atividade do paciente dentro do SISAC
    # Onde os 6 primeiros dígitos compõem o número do prontuário,
    # E o final, separado por um ponto(.), é a sequência do registro.
    # Exemplo: Se a função receber o parâmetro '006049.10', retornará '006049.11'.
    def addcodmovimento(codmovimento):
        cut = codmovimento.split('.')
        seqadd = int(cut[1]) + 1
        if seqadd < 10:
            seqadd = '0' + str(seqadd)
        codfinal = cut[0] + '.' + str(seqadd)  

        return codfinal
    
    # Marca a hora de início da tarefa
    horainicial = datetime.now()

    print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Consultando agenda MOSAIQ...')
    
    # Consulta na tabela Schedule do MOSAIQ pacientes agendados para hoje com status 'C' Completed (significa que realizaram tratamento)
    query_mosaiq = Schedule.objects.filter(dataagenda__year=date.today().year, dataagenda__month=date.today().month, 
                                            dataagenda__day=date.today().day).filter(status=' C')
    
    print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Consulta concluída com sucesso.')
    print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Iniciando iteração no resultado da consulta...')

    #Inicia contador do número de iterações
    i = 0

    # Inicia iterações para cada resultado obtido pela consulta anterior
    for obj in query_mosaiq.iterator():
        print('---------------------------------------------')

        # Guarda o CPF e a Data do Agendamento coletados no MOSAIQ para buscar correspondência no banco de dados SISAC
        cpf_paciente = obj.id_paciente.cpf
        dataagenda_mosaiq = obj.dataagenda

        # Busca um paciente no cadastro do SISAC que contenha o mesmo CPF do cadastro no MOSAIQ
        codpac_sisac = Cadpaciente.objects.filter(cpf=cpf_paciente).first()

        # Verifica se o resultado da busca pelo CPF é válido. Se válido, inicia próxima etapa.
        if codpac_sisac is not None:     
            print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Iniciando execuções para o paciente', codpac_sisac)   

            # Verifica qual último código de movimento do paciente na tabela Entrada do SISAC,
            # Em seguida chama a função addcodmovimento para incrementar a sequência.
            # O resultado do incremento é utilizado posteriormente para gerar novos registros nas tabelas do SISAC.    
            ultimo_codmov = Entrada.objects.filter(codpaciente=codpac_sisac.pk).order_by('datahoraent').last()
            novo_codmov = addcodmovimento(str(ultimo_codmov))

            # Verifica na tabela Agenda do SISAC algum agendamento de radioterapia para o paciente na data de hoje.
            agenda_sisac = Agenda.objects.filter(codpaciente=codpac_sisac).filter(datahora__year=date.today().year, 
                                            datahora__month=date.today().month, datahora__day=date.today().day).filter(tipo='RAD').first()

            # Verifica se o resultado da busca na agenda é válido. Se válido, inicia próxima etapa.
            if agenda_sisac is not None:
                print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Gerando registro na tabela entrada...')

                # Gera registro de sessão de radioterapia na tabela entrada.
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

                # Seleciona Última Prescrição do Paciente
                prescricao = Radioterapia.objects.filter(codpaciente=codpac_sisac.pk).order_by('numpresc').last()

                # Verifica quantidade de sessões de radioterapia realizadas
                sessoesrealizadas = Entrada.objects.filter(codpaciente=codpac_sisac).filter(hist__icontains='Sessão de Radioterapia').count()

                # Verifica número de aplicações de radioterapia para a fase 1
                naplicfase1 = Planejfisicoc.objects.filter(numpresc=prescricao).order_by('fase').first().naplicacoes

                # Se houver fase 2, define número de aplicações da fase 2
                if Planejfisicoc.objects.filter(numpresc=prescricao).order_by('fase').last().fase > 1:
                    naplicfase2 = Planejfisicoc.objects.filter(numpresc=prescricao).order_by('fase').last().naplicacoes
                
                # Define fase atual baseado na quantidade de sessões realizadas. 
                # Se quantidade realizada for menor que total de aplicações da Fase 1, então Fase = 1
                # Se quantidade realizada for maior ou igual ao total de aplicações da Fase 1, então Fase = 2
                if sessoesrealizadas < naplicfase1:
                    fase = Planejfisicoc.objects.filter(numpresc=prescricao).order_by('fase').first().fase        
                else:
                    fase = Planejfisicoc.objects.filter(numpresc=prescricao).order_by('fase').last().fase
                
                # Seleciona planejamento da prescrição, filtrando pela fase.
                planejamento = Planejfisico.objects.filter(numpresc=prescricao.pk).order_by('idplanejfisico').filter(fase=fase)

                print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Busca concluída.')
                print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Iniciando iteração no resultado da busca...')
                n = 0
                print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Gerando registros na tabela EntradaRadio...')

                # Inicia iterações sobre o resultado da consulta na tabela PlanejFisico.
                # O planejamento contém detalhes técnicos de cada um dos campos que paciente irá realizar.
                # Para cada campo encontrado no planejamento, a interação irá gerar um registro na tabela EntradaRadio,
                # Referênciando os detalhes técnicos presentes no planejamento e na prescrição médica.
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

                # Todas as etapas acima realizadas, finalmente acessa o agendamento de radioterapia localizada no início da tarefa,
                # Marca como confirmado, atribuindo 'S' na coluna ConfAtd e inserindo o código de movimento gerado pela função addcodmovimento,
                # Que faz referência o histórico gerado para o paciente nas etapas anteriores.
                agenda_sisac.confatd = 'S'
                agenda_sisac.usuario = 'API'
                agenda_sisac.codmovimento = novo_codmov
                agenda_sisac.datasist = datetime.now()
                agenda_sisac.save()
                print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Paciente confirmado.')
                print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Iteração concluída para o paciente', codpac_sisac)
                
        i += 1
    print('---------------------------------------------')
    print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Atualização da agenda concluída com sucesso.', i, 'pacientes foram confirmados na agenda de tratamento de radioterapia SISAC.')

    # Marca a hora final e calcula tempo total decorrido.
    horafinal = datetime.now()
    tempodecorrido = horafinal - horainicial
    print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Tempo total decorrido:', tempodecorrido)

    # Consulta na agenda de radioterapia do SISAC se possui algum paciente que não foi confirmado
    query_sisac2 = Agenda.objects.filter(datahora__year=date.today().year, datahora__month=date.today().month, 
                                            datahora__day=date.today().day).filter(~Q(confatd='S')).filter(tipo='RAD')

    # Se houver algum paciente não confirmado,
    # Itera sobre o resultado, adicionando os pacientes não tratados em uma lista    
    list = []
    if query_sisac2 is not None:
        for obj in query_sisac2.iterator():
            list.append(str(obj.codpaciente_id) + ' - ' + str(obj.codpaciente))
        print(str(len(list)), 'paciente(s) não confirmado(s):', str(list), ' Verifique se houve tratamento realizado para o(s) paciente(s) informado(s) em', date.today().strftime("%d/%m/%Y") + '.')

    # Se houver paciente não confirmado na agenda do SISAC, chama a função sendmail_lista,
    # Que enviará email de relatório contendo a quantidade de pacientes tratados e a lista de pacientes não confirmados.
    # Se todos os pacientes foram confirmados, chama a função sendmail,
    # Que enviará email de relatório contendo a quantidade de pacientes tratados.
    if len(list) > 0:
        sendmail_lista(list, i, datetime.now())
    else:
        sendmail(i, datetime.now())

    
