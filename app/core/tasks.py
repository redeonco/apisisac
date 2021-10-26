from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from celery import shared_task
from mosaiq_app.models import *
from core.models import (
    Agenda, 
    Cadpaciente, 
    Entrada, 
    Entradaradio, 
    Planejfisico, 
    Radioterapia, 
    Planejfisicoc,
    PrescrRadio
    )
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

@shared_task
def sendmail_cria_agenda(tarefa, msg):
    send_mail(
        'Núcleo de Sistemas - Relatório API - SISAC',
        'Núcleo de Sistemas - Relatório API - SISAC. \n Olá. Segue resumo da execução da tarefa ' + tarefa + ', em ' + datetime.now().strftime("%d/%m/%Y às %H:%M:%S") +
        '. \nA tarefa retornou a seguinte resposta: ' + msg + '.',
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
                                            dataagenda__day=date.today().day).filter(~Q(activity='MV')).filter(status=' C').filter(version=0).filter(~Q(suppressed=1))
    
    print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Consulta concluída com sucesso.')
    print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Iniciando iteração no resultado da consulta...')

    #Inicia contador do número de iterações
    i = 0

    # Inicia iterações para cada resultado obtido pela consulta anterior
    for obj in query_mosaiq.iterator():
        # Guarda o CPF e a Data do Agendamento coletados no MOSAIQ para buscar correspondência no banco de dados SISAC
        cpf_paciente = obj.id_paciente.cpf
        dataagenda_mosaiq = obj.dataagenda

        # Busca um paciente no cadastro do SISAC que contenha o mesmo CPF do cadastro no MOSAIQ
        codpac_sisac = Cadpaciente.objects.filter(cpf=cpf_paciente).first()
        
        # Verifica se o resultado da busca pelo CPF é válido. Se válido, inicia próxima etapa.
        if codpac_sisac is not None:     
            # Verifica qual último código de movimento do paciente na tabela Entrada do SISAC,
            # Em seguida chama a função addcodmovimento para incrementar a sequência.
            # O resultado do incremento é utilizado posteriormente para gerar novos registros nas tabelas do SISAC.    
            ultimo_codmov = Entrada.objects.filter(codpaciente=codpac_sisac.pk).order_by('datahoraent').last()
            print(ultimo_codmov)
            print(codpac_sisac)
            novo_codmov = addcodmovimento(str(ultimo_codmov))

            # Verifica na tabela Agenda do SISAC algum agendamento de radioterapia para o paciente na data de hoje.
            agenda_sisac = Agenda.objects.filter(codpaciente=codpac_sisac).filter(datahora__year=date.today().year, 
                                            datahora__month=date.today().month, datahora__day=date.today().day).filter(tipo='RAD').filter(~Q(confatd='S')).first()
            
            # Verifica se o resultado da busca na agenda é válido. Se válido, inicia próxima etapa.
            if agenda_sisac is not None:                
                print('---------------------------------------------')
                print('['+ datetime.now().strftime("%d/%m/%Y - %H:%M:%S") + ']', 'Iniciando execuções para o paciente', codpac_sisac) 
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
    # if len(list) > 0:
    #     sendmail_lista(list, i, datetime.now())
    # else:
    #    sendmail(i, datetime.now())


@shared_task
def atualiza_planej():
    # Localiza planejamentos no MOSAIQ que aprovados na data de hoje.
    # Não significa que geraram uma nova versão do tratamento
    # Pois para pacientes novos, a data de Criação é igual à data de Aprovação
    campos = TxField.objects.filter(version=0).filter(dose_campo__gt=0).filter(sanct_dt__year=date.today().year, sanct_dt__month=date.today().month, sanct_dt__day=date.today().day)

   # Inicializa um dicionário para as unidades de medida da energia do tratamento
    energia_unidade_dict = {
        '0': '',
        '1': 'KV',
        '2': 'MV',
        '3': 'MeV'
        }

    # Função para verificar se a fase inicia ao mesmo tempo que outra
    # A função verifica se existe um objeto relacionado na tabela fase
    # Na coluna reference_sit_set_id. Este coluna aponta para ID de outra fase
    # Indicando que as duas estão relacionadas.
    # Se este for o caso, a coluna Reference_Fraction determina o número da sessão de início desta fase, relacionada à outra
    # E a função retornará o ID da fase relacionada
    # Se ocorrer a exceção ObjectDoesNotExist, a função retornará False
    def checafase(fase):
        try:
            fase.reference_sit_set_id
            return fase.reference_sit_set_id
        except ObjectDoesNotExist:
            return False

    i = 0
    for obj in campos.iterator():
        i += 1
        print('iteração campo', i, obj)

        codpac_sisac = Cadpaciente.objects.exclude(cpf='').filter(cpf=obj.id_paciente.cpf).order_by('datasist').last()

        if codpac_sisac is not None:
            print('paciente encontrado')
            planejfisicoc = Planejfisicoc.objects.filter(codpaciente=codpac_sisac).filter(ncampo=obj.numero_campo).filter(fase=obj.id_fase.numerofase).filter(ativo=1)

            if planejfisicoc.count() > 0:
                print('planejamento encontrado para o paciente', codpac_sisac, 'numero do campo', obj.numero_campo)
                for planej2 in planejfisicoc.iterator():
                    planej2.energia = str(obj.txfieldpoint_set.first().energia) + energia_unidade_dict[str(obj.txfieldpoint_set.first().energia_unidade)]
                    planej2.dtt = obj.id_fase.dosetotal
                    planej2.dtd = obj.dose_campo
                    planej2.locanatomica = obj.id_fase.locanatomica
                    planej2.unidade_monitora = obj.unidade_monitora
                    planej2.ordemcampo = obj.numero_campo
                    planej2.fase = obj.id_fase.numerofase
                    planej2.incidencia = '3D'
                    planej2.tpfeixe = obj.id_fase.modalidade
                    planej2.save()
            else:
                print('planejamento NÃO encontrado para o paciente', codpac_sisac, 'numero do campo', obj.numero_campo)
                print('gerando registro na tabela PlanejFisicoC')
                print(obj)
                novo_planejfisicoc = Planejfisicoc()
                novo_planejfisicoc.codpaciente = codpac_sisac
                novo_planejfisicoc.codmovimento = codpac_sisac.codpaciente
                novo_planejfisicoc.numpresc = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last()
                novo_planejfisicoc.energia = str(obj.txfieldpoint_set.first().energia) + energia_unidade_dict[str(obj.txfieldpoint_set.first().energia_unidade)]
                novo_planejfisicoc.dtt = obj.id_fase.dosetotal
                novo_planejfisicoc.dtd = obj.dose_campo
                novo_planejfisicoc.naplicacoes = obj.id_fase.qtdsessoes
                novo_planejfisicoc.datasist = datetime.now()
                novo_planejfisicoc.ativo = 1
                novo_planejfisicoc.unidade_monitora = obj.unidade_monitora
                novo_planejfisicoc.nplanejamento = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().ntratamento
                novo_planejfisicoc.ntratamento = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().ntratamento
                novo_planejfisicoc.locanatomica = obj.id_fase.locanatomica
                novo_planejfisicoc.ncampo = obj.numero_campo
                novo_planejfisicoc.ordemcampo = obj.numero_campo

                # Verifica se a fase está relacionada com outra para definir o início do tratamento
                # Se não houver fase relacionada, inicio tratamento = 1
                # Se houver, define início tratamento com o valor obtido da coluna Reference_Fraction, tabela Fase
                if checafase(obj.id_fase) == False:
                    if obj.id_fase.numerofase == 1:
                        iniciotrat = 1
                    else:
                        fases = Fase.objects.filter(pcp_id=obj.id_fase.pcp_id).order_by('numerofase')
                        list_fases = []
                        for fas in fases:
                            list_fases.append(fas)
                        faseanterior = list_fases[list_fases.index(obj.id_fase) - 1]
                        iniciotrat = faseanterior.qtdsessoes + 1
                        
                else:
                    iniciotrat = obj.id_fase.reference_fraction

                novo_planejfisicoc.iniciotrat = iniciotrat
                novo_planejfisicoc.incidencia = '3D'
                novo_planejfisicoc.tpfeixe = obj.id_fase.modalidade
                novo_planejfisicoc.fase = obj.id_fase.numerofase
                novo_planejfisicoc.usuario = 'API'
                novo_planejfisicoc.save()

            planejfisico = Planejfisico.objects.filter(codpaciente=codpac_sisac).filter(ncampo=obj.numero_campo).filter(fase=obj.id_fase.numerofase).filter(ativo=1)

            if planejfisico.count() > 0:
                for planej in planejfisico:
                    planej.incidencia = '3D'
                    planej.nomecampo = obj.nome_campo
                    planej.ncampo = obj.numero_campo
                    planej.dtt = obj.id_fase.dosetotal
                    planej.dtd = obj.dose_campo
                    planej.fase = obj.id_fase.numerofase
                    planej.unidade_monitora = obj.unidade_monitora
                    planej.energia = str(obj.txfieldpoint_set.first().energia) + energia_unidade_dict[str(obj.txfieldpoint_set.first().energia_unidade)]
                    planej.tecnica = obj.id_fase.tecnica
                    planej.angulacao = 'G-' + str(obj.txfieldpoint_set.first().gantry) + ';M-000;C-' + str(obj.txfieldpoint_set.first().colimador)
                    planej.save()
            else:
                novo_planejfisico = Planejfisico()
                novo_planejfisico.idplanejfisicoc = Planejfisicoc.objects.filter(codpaciente=codpac_sisac).order_by('idplanejfisicoc').last()
                novo_planejfisico.codpaciente = codpac_sisac
                novo_planejfisico.codmovimento = codpac_sisac.codpaciente
                novo_planejfisico.numpresc = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last()
                novo_planejfisico.incidencia = '3D'
                novo_planejfisico.energia = str(obj.txfieldpoint_set.first().energia) + energia_unidade_dict[str(obj.txfieldpoint_set.first().energia_unidade)]
                novo_planejfisico.tecnica = obj.id_fase.tecnica
                novo_planejfisico.unidade_monitora = obj.unidade_monitora
                novo_planejfisico.angulacao = 'G-' + str(obj.txfieldpoint_set.first().gantry) + ';M-000;C-' + str(obj.txfieldpoint_set.first().colimador)
                novo_planejfisico.nplanejamento = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().ntratamento
                novo_planejfisico.ntratamento = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().ntratamento
                novo_planejfisico.ncampo = obj.numero_campo
                novo_planejfisico.fase = obj.id_fase.numerofase
                novo_planejfisico.ativo = 1
                novo_planejfisico.datasist = datetime.now()
                novo_planejfisico.dtt = obj.id_fase.dosetotal
                novo_planejfisico.dtd = obj.dose_campo
                novo_planejfisico.nomecampo = obj.nome_campo
                novo_planejfisico.usuario = 'API'
                novo_planejfisico.save()

            prescrradio = PrescrRadio.objects.filter(codpaciente=codpac_sisac).filter(numpresc=Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last()).filter(tratado='NAO').filter(fase=obj.id_fase.numerofase).filter(ncampos=obj.numero_campo)

            if prescrradio.count() > 0:
                for presc in prescrradio:
                    presc.ncampos = obj.numero_campo
                    presc.locanatomica = obj.id_fase.locanatomica
                    presc.datasist = datetime.now()
                    presc.incidencia = '3D'
                    presc.naplicacoes = obj.id_fase.qtdsessoes
                    presc.tecnica = obj.id_fase.tecnica
                    presc.tpfeixe = obj.id_fase.modalidade
                    presc.dosettotal = obj.id_fase.dosetotal
                    presc.dosetdiaria = obj.dose_campo
                    presc.energia = str(obj.txfieldpoint_set.first().energia) + energia_unidade_dict[str(obj.txfieldpoint_set.first().energia_unidade)]
                    presc.usuario = 'API'
                    presc.save()
            else:
                novapresc = PrescrRadio()
                novapresc.ncampos = obj.numero_campo
                novapresc.idradio = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().idradio
                novapresc.codmovimento = codpac_sisac.codpaciente
                novapresc.locanatomica = obj.id_fase.locanatomica
                novapresc.datasist = datetime.now()
                novapresc.numpresc = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last()
                novapresc.incidencia = '3D'
                novapresc.naplicacoes = obj.id_fase.qtdsessoes
                novapresc.ntratamento = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().ntratamento
                novapresc.codpaciente = codpac_sisac
                novapresc.usuario = 'API'
                novapresc.energia = str(obj.txfieldpoint_set.first().energia) + energia_unidade_dict[str(obj.txfieldpoint_set.first().energia_unidade)]
                novapresc.tecnica = obj.id_fase.tecnica
                novapresc.tpfeixe = obj.id_fase.modalidade
                novapresc.dosettotal = obj.id_fase.dosetotal
                novapresc.dosetdiaria = obj.dose_campo
                novapresc.fase = obj.id_fase.numerofase

                # Verifica se a fase está relacionada com outra para definir o início do tratamento
                # Se não houver fase relacionada, inicio tratamento = 1
                # Se houver, define início tratamento com o valor obtido da coluna Reference_Fraction, tabela Fase
                if checafase(obj.id_fase) == False:
                    if obj.id_fase.numerofase == 1:
                        iniciotrat = 1
                    else:
                        fases = Fase.objects.filter(pcp_id=obj.id_fase.pcp_id).order_by('numerofase')
                        list_fases = []
                        for fas in fases:
                            list_fases.append(fas)
                        faseanterior = list_fases[list_fases.index(obj.id_fase) - 1]
                        iniciotrat = faseanterior.qtdsessoes + 1
                        
                else:
                    iniciotrat = obj.id_fase.reference_fraction

                novapresc.iniciotrat = iniciotrat
                novapresc.save()

            primeira_agenda = Agenda.objects.filter(codpaciente=codpac_sisac).filter(tipo='RAD').filter(planejado='N').filter(confatd='N').order_by('idagenda').first()
            if primeira_agenda is not None:
                primeira_agenda.planejado = 'S'            
                primeira_agenda.save() 
                print(f'Alterado a agenda do paciente {codpac_sisac}, dia {primeira_agenda.datahora} com status Planejado OK.')
            else:
                pass
                                    

@shared_task
def força_atualiza_planej():
    # Localiza planejamentos no MOSAIQ que aprovados na data de hoje.
    # Não significa que geraram uma nova versão do tratamento
    # Pois para pacientes novos, a data de Criação é igual à data de Aprovação
    query_mosaiq = Schedule.objects.filter(dataagenda__year=date.today().year, dataagenda__month=date.today().month, 
                                            dataagenda__day=date.today().day).filter(version=0).filter(~Q(suppressed=1)).exclude(id_paciente=10084)
    pac = []
    for i in query_mosaiq:
        pac.append(i.id_paciente)

    campos = TxField.objects.filter(version=0).filter(dose_campo__gt=0).filter(id_paciente__in=pac)

    # Inicializa uma lista para os pacientes com tratamento versionado
    list_versionado = []

    # Inicializa um dicionário para as unidades de medida da energia do tratamento
    energia_unidade_dict = {
        '0': '',
        '1': 'KV',
        '2': 'MV',
        '3': 'MeV'
        }

    # Função para verificar se a fase inicia ao mesmo tempo que outra
    # A função verifica se existe um objeto relacionado na tabela fase
    # Na coluna reference_sit_set_id. Este coluna aponta para ID de outra fase
    # Indicando que as duas estão relacionadas.
    # Se este for o caso, a coluna Reference_Fraction determina o número da sessão de início desta fase, relacionada à outra
    # E a função retornará o ID da fase relacionada
    # Se ocorrer a exceção ObjectDoesNotExist, a função retornará False
    def checafase(fase):
        try:
            fase.reference_sit_set_id
            return fase.reference_sit_set_id
        except ObjectDoesNotExist:
            return False

    # Para cada resultado da busca anterior, realiza iteração 
    # for obj in campos:
        # Procura registros na tabela TxField, realizando consulta reversa pelo PCP_ID obtido da consulta anterior, filtrando onde versão é maior que 0
        # Versão 0 sempre é a atual. Quanto maior for o número, mais antiga é a versão do tratamento.
        # A ideia aqui é localizar na tabela Fase tratamentos que foram aprovados hoje, e que possuem versões antigas de tratamento
        # Significando que realmente o paciente sofreu alteração no planejamento
        # E para cada paciente com tratamendo alterado, algoritimo vai atualizar o histórico no SISAC com o novo planejamento
        # query = TxField.objects.filter(id_fase__pcp_id=obj.id_fase.pcp_id)# .filter(version__gt=0)
        # for i in query:
          #  list_versionado.append(i.id_fase.pcp_id_id)

    campos2 = campos.filter(id_fase__pcp_id__in=list_versionado).filter(version=0).filter(dose_campo__gt=0)

    i = 0
    for obj in campos.iterator():
        i += 1
        print('iteração campo', i)
        codpac_sisac = Cadpaciente.objects.exclude(cpf='').get(cpf=obj.id_paciente.cpf)
        if codpac_sisac is not None:
            print('paciente encontrado')
            planejfisicoc = Planejfisicoc.objects.filter(codpaciente=codpac_sisac).filter(ncampo=obj.numero_campo).filter(fase=obj.id_fase.numerofase).filter(ativo=1)

            if planejfisicoc.count() > 0:
                print('planejamento encontrado para o paciente', codpac_sisac, 'numero do campo', obj.numero_campo)
                for planej2 in planejfisicoc.iterator():
                    planej2.energia = str(obj.txfieldpoint_set.first().energia) + energia_unidade_dict[str(obj.txfieldpoint_set.first().energia_unidade)]
                    planej2.dtt = obj.id_fase.dosetotal
                    planej2.dtd = obj.dose_campo
                    planej2.locanatomica = obj.id_fase.locanatomica
                    planej2.unidade_monitora = obj.unidade_monitora
                    planej2.ordemcampo = obj.numero_campo
                    planej2.fase = obj.id_fase.numerofase
                    planej2.incidencia = '3D'
                    planej2.tpfeixe = obj.id_fase.modalidade
                    planej2.save()
            else:
                print('planejamento NÃO encontrado para o paciente', codpac_sisac, 'numero do campo', obj.numero_campo)
                print('gerando registro na tabela PlanejFisicoC')
                print(obj)
                novo_planejfisicoc = Planejfisicoc()
                novo_planejfisicoc.codpaciente = codpac_sisac
                novo_planejfisicoc.codmovimento = codpac_sisac.codpaciente
                novo_planejfisicoc.numpresc = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last()
                novo_planejfisicoc.energia = str(obj.txfieldpoint_set.first().energia) + energia_unidade_dict[str(obj.txfieldpoint_set.first().energia_unidade)]
                novo_planejfisicoc.dtt = obj.id_fase.dosetotal
                novo_planejfisicoc.dtd = obj.dose_campo
                novo_planejfisicoc.naplicacoes = obj.id_fase.qtdsessoes
                novo_planejfisicoc.datasist = datetime.now()
                novo_planejfisicoc.ativo = 1
                novo_planejfisicoc.unidade_monitora = obj.unidade_monitora
                novo_planejfisicoc.nplanejamento = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().ntratamento
                novo_planejfisicoc.ntratamento = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().ntratamento
                novo_planejfisicoc.locanatomica = obj.id_fase.locanatomica
                novo_planejfisicoc.ncampo = obj.numero_campo
                novo_planejfisicoc.ordemcampo = obj.numero_campo

                # Verifica se a fase está relacionada com outra para definir o início do tratamento
                # Se não houver fase relacionada, inicio tratamento = 1
                # Se houver, define início tratamento com o valor obtido da coluna Reference_Fraction, tabela Fase
                if checafase(obj.id_fase) == False:
                    if obj.id_fase.numerofase == 1:
                        iniciotrat = 1
                    else:
                        fases = Fase.objects.filter(pcp_id=obj.id_fase.pcp_id).order_by('numerofase')
                        list_fases = []
                        for fas in fases:
                            list_fases.append(fas)
                        faseanterior = list_fases[list_fases.index(obj.id_fase) - 1]
                        iniciotrat = faseanterior.qtdsessoes + 1
                        
                else:
                    iniciotrat = obj.id_fase.reference_fraction

                novo_planejfisicoc.iniciotrat = iniciotrat
                novo_planejfisicoc.incidencia = '3D'
                novo_planejfisicoc.tpfeixe = obj.id_fase.modalidade
                novo_planejfisicoc.fase = obj.id_fase.numerofase
                novo_planejfisicoc.usuario = 'API'
                novo_planejfisicoc.save()

            planejfisico = Planejfisico.objects.filter(codpaciente=codpac_sisac).filter(ncampo=obj.numero_campo).filter(fase=obj.id_fase.numerofase).filter(ativo=1)

            if planejfisico.count() > 0:
                for planej in planejfisico:
                    planej.incidencia = '3D'
                    planej.nomecampo = obj.nome_campo
                    planej.ncampo = obj.numero_campo
                    planej.dtt = obj.id_fase.dosetotal
                    planej.dtd = obj.dose_campo
                    planej.fase = obj.id_fase.numerofase
                    planej.unidade_monitora = obj.unidade_monitora
                    planej.energia = str(obj.txfieldpoint_set.first().energia) + energia_unidade_dict[str(obj.txfieldpoint_set.first().energia_unidade)]
                    planej.tecnica = obj.id_fase.tecnica
                    planej.angulacao = 'G-' + str(obj.txfieldpoint_set.first().gantry) + ';M-000;C-' + str(obj.txfieldpoint_set.first().colimador)
                    planej.save()
            else:
                novo_planejfisico = Planejfisico()
                novo_planejfisico.idplanejfisicoc = Planejfisicoc.objects.filter(codpaciente=codpac_sisac).order_by('idplanejfisicoc').last()
                novo_planejfisico.codpaciente = codpac_sisac
                novo_planejfisico.codmovimento = codpac_sisac.codpaciente
                novo_planejfisico.numpresc = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last()
                novo_planejfisico.incidencia = '3D'
                novo_planejfisico.energia = str(obj.txfieldpoint_set.first().energia) + energia_unidade_dict[str(obj.txfieldpoint_set.first().energia_unidade)]
                novo_planejfisico.tecnica = obj.id_fase.tecnica
                novo_planejfisico.unidade_monitora = obj.unidade_monitora
                novo_planejfisico.angulacao = 'G-' + str(obj.txfieldpoint_set.first().gantry) + ';M-000;C-' + str(obj.txfieldpoint_set.first().colimador)
                novo_planejfisico.nplanejamento = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().ntratamento
                novo_planejfisico.ntratamento = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().ntratamento
                novo_planejfisico.ncampo = obj.numero_campo
                novo_planejfisico.fase = obj.id_fase.numerofase
                novo_planejfisico.ativo = 1
                novo_planejfisico.datasist = datetime.now()
                novo_planejfisico.dtt = obj.id_fase.dosetotal
                novo_planejfisico.dtd = obj.dose_campo
                novo_planejfisico.nomecampo = obj.nome_campo
                novo_planejfisico.usuario = 'API'
                novo_planejfisico.save()

            prescrradio = PrescrRadio.objects.filter(codpaciente=codpac_sisac).filter(numpresc=Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last()).filter(tratado='NAO').filter(fase=obj.id_fase.numerofase).filter(ncampos=obj.numero_campo)

            if prescrradio.count() > 0:
                for presc in prescrradio:
                    presc.ncampos = obj.numero_campo
                    presc.locanatomica = obj.id_fase.locanatomica
                    presc.datasist = datetime.now()
                    presc.incidencia = '3D'
                    presc.naplicacoes = obj.id_fase.qtdsessoes
                    presc.tecnica = obj.id_fase.tecnica
                    presc.tpfeixe = obj.id_fase.modalidade
                    presc.dosettotal = obj.id_fase.dosetotal
                    presc.dosetdiaria = obj.dose_campo
                    presc.energia = str(obj.txfieldpoint_set.first().energia) + energia_unidade_dict[str(obj.txfieldpoint_set.first().energia_unidade)]
                    presc.usuario = 'API'
                    presc.save()
            else:
                novapresc = PrescrRadio()
                novapresc.ncampos = obj.numero_campo
                novapresc.idradio = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().idradio
                novapresc.codmovimento = codpac_sisac.codpaciente
                novapresc.locanatomica = obj.id_fase.locanatomica
                novapresc.datasist = datetime.now()
                novapresc.numpresc = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last()
                novapresc.incidencia = '3D'
                novapresc.naplicacoes = obj.id_fase.qtdsessoes
                novapresc.ntratamento = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().ntratamento
                novapresc.codpaciente = codpac_sisac
                novapresc.usuario = 'API'
                novapresc.energia = str(obj.txfieldpoint_set.first().energia) + energia_unidade_dict[str(obj.txfieldpoint_set.first().energia_unidade)]
                novapresc.tecnica = obj.id_fase.tecnica
                novapresc.tpfeixe = obj.id_fase.modalidade
                novapresc.dosettotal = obj.id_fase.dosetotal
                novapresc.dosetdiaria = obj.dose_campo
                novapresc.fase = obj.id_fase.numerofase

                # Verifica se a fase está relacionada com outra para definir o início do tratamento
                # Se não houver fase relacionada, inicio tratamento = 1
                # Se houver, define início tratamento com o valor obtido da coluna Reference_Fraction, tabela Fase
                if checafase(obj.id_fase) == False:
                    if obj.id_fase.numerofase == 1:
                        iniciotrat = 1
                    else:
                        fases = Fase.objects.filter(pcp_id=obj.id_fase.pcp_id).order_by('numerofase')
                        list_fases = []
                        for fas in fases:
                            list_fases.append(fas)
                        faseanterior = list_fases[list_fases.index(obj.id_fase) - 1]
                        iniciotrat = faseanterior.qtdsessoes + 1
                        
                else:
                    iniciotrat = obj.id_fase.reference_fraction

                novapresc.iniciotrat = iniciotrat
                novapresc.save()


def cria_agenda_radio():
    # Função para gerar nova senha da agenda. Pega a última senha existente e adiciona 1
    def senhanova():
        ultimasenha = Agenda.objects.last().senha # 0006001
        novasenha = int(ultimasenha) + 1
        zeros = 7 - len(str(novasenha)) 
        senhafinal = '0' * zeros + str(novasenha)

        return senhafinal


    agenda_mosaiq_dia = Schedule.objects.filter(dataagenda__year=date.today().year, dataagenda__month=date.today().month, dataagenda__day=date.today().day).filter(activity='3D').filter(version=0).filter(~Q(suppressed=1))

    agendamento_existente = []

    for pac in agenda_mosaiq_dia:
        codpac_sisac = Cadpaciente.objects.get(cpf=pac.id_paciente.cpf)
        if codpac_sisac is not None:
            primeira_agenda = Agenda.objects.filter(codpaciente=codpac_sisac).filter(tipo='RAD').filter(planejado='S')
            if primeira_agenda.count() <= 1:
                primeira_agenda.tipo = ''
                primeira_agenda.tipooriginal = ''
                primeira_agenda.save()
                agenda_mosaiq = Schedule.objects.filter(id_paciente=pac.id_paciente).filter(activity='3D').filter(~Q(suppressed=1))
                for agd in agenda_mosaiq:
                    checa_agenda = Agenda.objects.filter(datahora=agd.dataagenda).filter(tipo='RAD')
                    if checa_agenda.count() > 0:
                        print(f'Já existe agendamento no dia {agd.dataagenda.strftime("%d/%m/%Y - %H:%M:%S")}.')
                        dict = {}
                        dict['IDAgenda_SISAC'] = checa_agenda.first().idagenda
                        dict['Paciente'] = str(checa_agenda.first().codpaciente.codpaciente) + ' - ' + str(checa_agenda.first().codpaciente.paciente)
                        dict['DataHora_Existente'] = checa_agenda.first().datahora.strftime("%d/%m/%Y - %H:%M:%S")
                        dict['Tentou_Encaixar'] = str(codpac_sisac.codpaciente) + ' - ' + str(codpac_sisac.paciente)
                        agendamento_existente.append(dict)
                    else:
                        agenda = Agenda()
                        agenda.codmedico = '103'
                        agenda.datahora = agd.dataagenda
                        agenda.nome = codpac_sisac.paciente
                        agenda.codconvenio = Entrada.objects.filter(codpaciente=codpac_sisac).order_by('datahoraent').last().codconvenio
                        agenda.codpaciente = codpac_sisac
                        agenda.obs = 'Sessão de Radioterapia'
                        agenda.usuario = 'API'
                        agenda.descr = Entrada.objects.filter(codpaciente=codpac_sisac).order_by('datahoraent').last().codconvenio.descr
                        agenda.datasist = datetime.now()
                        agenda.confatd = 'N'
                        agenda.tipo = 'RAD'
                        agenda.plano = Entrada.objects.filter(codpaciente=codpac_sisac).order_by('datahoraent').last().plano
                        agenda.telefone = codpac_sisac.telefone2
                        senha = senhanova()
                        agenda.senha = senha
                        agenda.ntratradio = Radioterapia.objects.filter(codpaciente=codpac_sisac).last().ntratamento
                        agenda.planejado = 'S'
                        agenda.whatsapp = codpac_sisac.whatsapp
                        agenda.tipooriginal = 'RAD'
                        agenda.save()

    if len(agendamento_existente) > 0:
        msg = f'A tarefa de criação de agenda automática do SISAC reportou existência de agendamentos existentes. \nViolação de integridade foi evitada para o(s) seguinte(s) agendamento(s):{agendamento_existente}'
        sendmail_cria_agenda('Cria Agenda Radio SISAC', msg)


def atualiza_datahora_agenda():
    violacao = []
    sem_agenda_sisac = []
    atualizados = []
    agenda_mosaiq = Schedule.objects.filter(dataagenda__gte=date.today()).order_by('dataagenda').filter(activity='3D').filter(~Q(status=' C')).filter(version=0).filter(~Q(suppressed=1))
    for pac in agenda_mosaiq:
        print(f'Encontrado agenda MOSAIQ para o paciente {pac.id_paciente} dia {pac.dataagenda}')
        codpac_sisac = Cadpaciente.objects.get(cpf=pac.id_paciente.cpf)
        if codpac_sisac is not None:
            print(f'Encontrado relacinamento para o paciente {codpac_sisac} no SISAC.')
            agenda_sisac = Agenda.objects.filter(codpaciente=codpac_sisac).filter(tipo='RAD').filter(confatd='N').filter(datahora__year=pac.dataagenda.year, datahora__month=pac.dataagenda.month, datahora__day=pac.dataagenda.day).first()
            if agenda_sisac is not None:
                print(f'Encontrado agenda para o paciente {codpac_sisac}, dia {agenda_sisac.datahora}')
                if agenda_sisac.datahora == pac.dataagenda:
                    print(f'Agendamento no SISAC é igual ao agendamento no MOSAIQ... Nada a fazer.')
                    print('---------------------------------------------------')
                else:
                    agenda_dia = Agenda.objects.filter(tipo='RAD').filter(datahora=pac.dataagenda)
                    if agenda_dia.count() > 0:
                        print(f'Paciente {agenda_dia.first().codpaciente} ocupando o horário {pac.dataagenda}. A alteração forçada provocaria violação de integridade.')
                        print('---------------------------------------------------')
                        dict = {}
                        dict['CodPaciente'] = str(codpac_sisac.codpaciente) + ' - ' + str(codpac_sisac.paciente)
                        dict['DataHora_Atual'] = agenda_sisac.datahora.strftime("%d/%m/%Y - %H:%M:%S")
                        dict['DataHora_MOSAIQ'] = pac.dataagenda.strftime("%d/%m/%Y - %H:%M:%S")
                        dict['Ocupado_Por'] = str(agenda_dia.first().codpaciente.codpaciente) + ' - ' + str(agenda_dia.first().codpaciente.paciente)
                        violacao.append(dict)
                    else:
                        agenda_sisac.datahora = pac.dataagenda
                        agenda_sisac.save()
                        print(f'Agendamento ID {agenda_sisac.idagenda} SISAC Atualizada. Data/hora antiga: {agenda_sisac.datahora}. Data/Hora nova: {pac.dataagenda}')
                        print('---------------------------------------------------')
                        dict = {}
                        dict['CodPaciente'] = str(codpac_sisac.codpaciente) + ' - ' + str(codpac_sisac.paciente)
                        dict['IDAgenda_SISAC'] = agenda_sisac.idagenda
                        dict['DataHora_Atualizada'] = pac.dataagenda.strftime("%d/%m/%Y - %H:%M:%S")
                        atualizados.append(dict)
            else:
                print(f'Nenhum agendamento no SISAC encontrado para o paciente {codpac_sisac} no dia {pac.dataagenda}')
                print('---------------------------------------------------')
                dict = {}
                dict['CodPaciente'] = str(codpac_sisac.codpaciente) + ' - ' + str(codpac_sisac.paciente)
                dict['DataHora_MOSAIQ'] = pac.dataagenda.strftime("%d/%m/%Y - %H:%M:%S")
                sem_agenda_sisac.append(dict)
    print('---------------------------------------------------')
    print('Procedimento concluído')
    print(f'Segue lista de violações de integridade encontradas: {violacao}')
    print(f'Segue lista de agendamentos sem referência no SISAC: {sem_agenda_sisac}')
    print(f'Segue lista de agendamentos atualizados no SISAC: {atualizados}')

    msg = f'Segue lista de violações de integridade encontradas: {violacao}. \n\nSegue lista de agendamentos sem referência no SISAC: {sem_agenda_sisac}. \n\nSegue lista de agendamentos atualizados no SISAC: {atualizados}'
    sendmail_cria_agenda('Atualiza Agenda Radio SISAC', msg)

