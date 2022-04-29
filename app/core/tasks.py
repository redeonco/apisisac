from typing import List

from django.core.exceptions import ObjectDoesNotExist
from core.functions import *
from celery import shared_task
from config.models import TAB_Parametro
from core.models import CadConvenio, Exame, Fatura, TabAmb
from mosaiq_app.models import *
from control.models import *
from core.models import (
    Agenda, 
    Cadpaciente, 
    Entrada, 
    Entradaradio, 
    Planejfisico, 
    Radioterapia, 
    Planejfisicoc,
    PrescrRadio,
    SolicExa
    )
from datetime import datetime, date
from django.db.models import Q
from django.core.mail import send_mail
# from .logger import API_LOGGER
from core.resources.constants import API_USER

'''
 Tarefa para atualizar a agenda de tratamento da radioterapia do SISAC comparando com a agenda de tratamento do MOSAIQ
 A tarefa olha para a agenda do MOSAIQ quais pacientes estão marcados como Completed
 Para cada paciente marcado como Completed, a tarefa realiza iterações no banco de dados SISAC
 Gerando registros na tabela Entrada, EntradaRadio e Agenda
 Confirmando na agenda de radioterapia do SISAC os pacientes tratados no MOSAIQ
'''
@shared_task
def atualizaagenda():
    # Marca a hora de início da tarefa
    horainicial = datetime.now()

    print('Consultando agenda MOSAIQ...')
    
    # Consulta na tabela Schedule do MOSAIQ pacientes agendados para hoje com status 'C' Completed (significa que realizaram tratamento)
    query_mosaiq = Schedule.objects.filter(dataagenda__year=date.today().year, dataagenda__month=date.today().month, 
                                            dataagenda__day=date.today().day).filter(~Q(activity='MV')).filter(status=' C').filter(version=0).filter(~Q(suppressed=1))
    
    print('[ATUALIZA_AGENDA] - Consulta concluída com sucesso.')
    print('[ATUALIZA_AGENDA] - Iniciando iteração no resultado da consulta...')

    #Inicia contador do número de iterações
    i = 0

    # Inicia iterações para cada resultado obtido pela consulta anterior
    for obj in query_mosaiq.iterator():
        # Guarda o CPF e a Data do Agendamento coletados no MOSAIQ para buscar correspondência no banco de dados SISAC
        cpf_paciente = obj.id_paciente.cpf
        dataagenda_mosaiq = obj.dataagenda

        # Realiza chamada na função relaciona_paciente(), passando como parâmetro um objeto da classe Patient MOSAIQ
        # Se encontrar um paciente relacionado no SISAC, a função vai retornar o objeto Cadpaciente
        # Se não encontrar paciente, a função vai retornar False.
        codpac_sisac = relaciona_paciente(obj.id_paciente)
        
        # Verifica se o resultado da busca pelo CPF é válido. Se válido, inicia próxima etapa.
        if codpac_sisac:     
            # Verifica qual último código de movimento do paciente na tabela Entrada do SISAC,
            # Em seguida chama a função addcodmovimento para incrementar a sequência.
            # O resultado do incremento é utilizado posteriormente para gerar novos registros nas tabelas do SISAC.    
            ultimo_codmov = Entrada.objects.filter(codpaciente=codpac_sisac.pk).filter(filial='01').order_by('natendimento').last()
            novo_codmov = addcodmovimento(str(ultimo_codmov))

            # Verifica na tabela Agenda do SISAC algum agendamento de radioterapia para o paciente na data de hoje.
            agenda_sisac = Agenda.objects.filter(codpaciente=codpac_sisac).filter(datahora__year=date.today().year, 
                                            datahora__month=date.today().month, datahora__day=date.today().day).filter(tipo='RAD').filter(~Q(confatd='S')).first()
            
            # Seleciona Última Prescrição do Paciente
            prescricao = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last()

            # Seleciona Solicitação de tratamento realizada pelo médico
            solic_tto = SolicExa.objects.filter(npresc=prescricao.numpresc).order_by('item').first()

            # Verifica número de aplicações de radioterapia para a fase 1
            planejamentoc = Planejfisicoc.objects.filter(numpresc=prescricao.numpresc).order_by('fase').first()
            
            # Verifica se o resultado da busca na agenda é válido. Se válido, inicia próxima etapa.
            if agenda_sisac is not None:
                print(f'[ATUALIZA_AGENDA] - Paciente {codpac_sisac} possui agendamento para hoje.')
                print(f'[ATUALIZA_AGENDA] - Verificando existência de prescriçao e planejamento...')
                if (
                    prescricao is not None 
                    and planejamentoc is not None
                    ):
                    print('[ATUALIZA_AGENDA] - Iniciando execuções para o paciente', codpac_sisac) 
                    print('[ATUALIZA_AGENDA] - Gerando registro na tabela entrada...')

                    # Gera registro de sessão de radioterapia na tabela entrada.
                    entrada = Entrada()
                    entrada.codpaciente = codpac_sisac
                    entrada.codmovimento = novo_codmov
                    entrada.tipo = '4'
                    entrada.fechado = 'E'
                    entrada.datahoraent = dataagenda_mosaiq
                    entrada.datasist = datetime.now()
                    entrada.local = ''
                    entrada.usuario = API_USER
                    entrada.recep = API_USER
                    entrada.codconvenio = CadConvenio.objects.get(solic_tto.codconvenio)
                    entrada.plano = ''
                    entrada.codmedico = solic_tto.codmedico
                    entrada.hist = 'Sessão de Radioterapia'
                    entrada.total = 0
                    entrada.grupoemp = '01'
                    entrada.filial = '01'
                    novocodigo_natendimento = incrementa_natendimento()
                    entrada.natendimento = novocodigo_natendimento
                    entrada.save()
                    print('[ATUALIZA_AGENDA] - Registro gerado na tabela entrada.')

                    print('[ATUALIZA_AGENDA] - Buscando registros de prescrição e planejamento...')

                    # Seleciona Última Prescrição do Paciente
                    prescricao = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last()

                    # Verifica quantidade de sessões de radioterapia realizadas
                    sessoesrealizadas = Agenda.objects.filter(tipo='RAD').filter(confatd='S').filter(codpaciente=codpac_sisac).count()
                    
                    # Verifica número de aplicações de radioterapia para a fase 1
                    planejamentoc = Planejfisicoc.objects.filter(numpresc=prescricao.numpresc).order_by('fase').first()

                    naplicfase1 = planejamentoc.naplicacoes

                    # Se houver fase 2, define número de aplicações da fase 2
                    if Planejfisicoc.objects.filter(numpresc=prescricao.numpresc).order_by('fase').last().fase > 1:
                        naplicfase2 = Planejfisicoc.objects.filter(numpresc=prescricao.numpresc).order_by('fase').last().naplicacoes
                    
                    # Define fase atual baseado na quantidade de sessões realizadas. 
                    # Se quantidade realizada for menor que total de aplicações da Fase 1, então Fase = 1
                    # Se quantidade realizada for maior ou igual ao total de aplicações da Fase 1, então Fase = 2
                    if sessoesrealizadas < naplicfase1:
                        fase = Planejfisicoc.objects.filter(numpresc=prescricao.numpresc).order_by('fase').first().fase        
                    else:
                        fase = Planejfisicoc.objects.filter(numpresc=prescricao.numpresc).order_by('fase').last().fase
                    
                    # Seleciona planejamento da prescrição, filtrando pela fase.
                    planejamento = Planejfisico.objects.filter(numpresc=prescricao.numpresc).order_by('idplanejfisico').filter(fase=fase)

                    print('[ATUALIZA_AGENDA] - Busca concluída.')
                    print('[ATUALIZA_AGENDA] - Iniciando iteração no resultado da busca...')
                    n = 0
                    print('[ATUALIZA_AGENDA] - Gerando registros na tabela EntradaRadio...')


                    campostratados = Dose_Hst.objects.filter(id_paciente=obj.id_paciente).filter(datahora__year=date.today().year,datahora__month=date.today().month, datahora__day=date.today().day).filter(dose_campo__gt=0)


                    # Inicia iterações sobre o resultado da consulta na tabela PlanejFisico.
                    # O planejamento contém detalhes técnicos de cada um dos campos que paciente irá realizar.
                    # Para cada campo encontrado no planejamento, a interação irá gerar um registro na tabela EntradaRadio,
                    # Referênciando os detalhes técnicos presentes no planejamento e na prescrição médica.
                    for campo in campostratados:
                        try:                        
                            planej = Planejfisico.objects.get(id_mosaiq=campo.id_campo_id)              
                            entradaradio = Entradaradio()
                            entradaradio.codmovimento = novo_codmov
                            entradaradio.codpaciente = codpac_sisac.pk
                            entradaradio.numpresc = prescricao.numpresc
                            entradaradio.idplanejfisico = Planejfisico.objects.get(id_mosaiq=campo.id_campo_id).idplanejfisico
                            entradaradio.encerrado = 'S'
                            entradaradio.observacao = ''
                            entradaradio.usuario = API_USER
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
                        except Exception as e:
                            print(f'[ATUALIZA_AGENDA] - Erro durante gravaçao de registros na tabela EntradaRadio: {e}')
                    print('[ATUALIZA_AGENDA] - ', n, 'registro(s) gerado(s) na tabela EntradaRadio.')

                    print('[ATUALIZA_AGENDA] - Confirmando paciente na tabela Agenda Radioterapia...')

                    # Todas as etapas acima realizadas, finalmente acessa o agendamento de radioterapia localizada no início da tarefa,
                    # Marca como confirmado, atribuindo 'S' na coluna ConfAtd e inserindo o código de movimento gerado pela função addcodmovimento,
                    # Que faz referência o histórico gerado para o paciente nas etapas anteriores.
                    agenda_sisac.confatd = 'S'
                    agenda_sisac.usuario = API_USER
                    agenda_sisac.codmovimento = novo_codmov
                    agenda_sisac.datasist = datetime.now()
                    agenda_sisac.save()
                    print('[ATUALIZA_AGENDA] - Paciente confirmado.')
                    print('[ATUALIZA_AGENDA] - Iteração concluída para o paciente', codpac_sisac)

                    # Verifica a quantidade de sessões realizadas.
                    qtd_realizada = Agenda.objects.filter(tipo='RAD').filter(confatd='S').filter(codpaciente=codpac_sisac).count()


                    if qtd_realizada == 1:
                        codamb = SolicExa.objects.filter(npresc=prescricao.numpresc).order_by('item').first().codamb                    
                        print(f'[ATUALIZA_AGENDA] - Primeira sessão de radioterapia do paciente {codpac_sisac}. Iniciando lançamento do pacote do tratamento na conta do paciente...')                    
                        primeira_entrada = Entrada.objects.filter(codpaciente=codpac_sisac).filter(filial='01').order_by('datahoraent').first()
                        codconvenio = solic_tto.codconvenio
                        matricula = primeira_entrada.matricula
                        codmedico = solic_tto.codmedico
                        plano = primeira_entrada.plano
                        ultimo_codmov = Entrada.objects.filter(codpaciente=codpac_sisac).filter(filial='01').order_by('datahoraent').last()
                        novo_codmov = addcodmovimento(str(ultimo_codmov))
                        
                        # Gerar registro do pacote de tratamento na tabela Entrada
                        
                        if Entrada.objects.filter(codpaciente=codpac_sisac).filter(codamb=codamb).count() == 0:
                            entrada = Entrada()
                            entrada.codmovimento = novo_codmov
                            entrada.codpaciente = codpac_sisac
                            entrada.codconvenio = codconvenio
                            entrada.matricula = matricula
                            entrada.tipo = '4'
                            entrada.datahoraent = datetime.now()
                            entrada.hist = TabAmb.objects.filter(codamb=codamb).filter(codconvenio=codconvenio.hm).first().descr
                            entrada.codmedico = codmedico
                            entrada.local = '112'
                            entrada.recep = API_USER
                            entrada.total = TabAmb.objects.filter(codamb=codamb).filter(codconvenio=codconvenio.hm).first().ch
                            entrada.fechado = 'P'
                            entrada.codamb = codamb
                            entrada.datasist = datetime.now()
                            entrada.plano = plano
                            entrada.tabhm = CadConvenio.objects.get(codconvenio=codconvenio).hm
                            entrada.datahoraint = datetime.now()
                            entrada.localini = '112'
                            novocodigo_natendimento = incrementa_natendimento()
                            entrada.natendimento = novocodigo_natendimento
                            entrada.datamarcada = datetime.now()
                            entrada.save()

                        # Gerar registro do pacote de tratamento na tabela Fatura
                        if Fatura.objects.filter(codpaciente__icontains=codpac_sisac.codpaciente).filter(codamb=codamb).count() == 0:
                            fatura = Fatura()
                            fatura.codpaciente = novo_codmov
                            fatura.grupo = '1'
                            fatura.codtaxa = codamb
                            fatura.descr = TabAmb.objects.filter(codamb=codamb).filter(codconvenio=codconvenio.hm).first().descr
                            fatura.data = datetime.now()
                            fatura.valor = TabAmb.objects.filter(codamb=codamb).filter(codconvenio=codconvenio.hm).first().ch
                            fatura.quant = '1'
                            fatura.filme = '0'
                            fatura.codmedico = codmedico
                            fatura.datasist = datetime.now()
                            fatura.usuario = API_USER
                            fatura.codamb = codamb
                            fatura.ch = TabAmb.objects.filter(codamb=codamb).filter(codconvenio=codconvenio.hm).first().ch
                            fatura.local = '112'
                            fatura.honor = TabAmb.objects.filter(codamb=codamb).filter(codconvenio=codconvenio.hm).first().ch
                            fatura.vpprof = TabAmb.objects.filter(codamb=codamb).filter(codconvenio=codconvenio.hm).first().ch
                            fatura.obs = f'Tab.Honor {CadConvenio.objects.get(codconvenio=codconvenio).hm} {CadConvenio.objects.get(codconvenio=CadConvenio.objects.get(codconvenio=codconvenio).hm).descr}'
                            fatura.localac = '112'
                            fatura.save()

                        # Gerar registro do pacote de tratamento na tabela Exame
                        if Exame.objects.filter(codpaciente__icontains=codpac_sisac.codpaciente).filter(codamb=codamb).count() == 0:
                            exame = Exame()
                            exame.codpaciente = novo_codmov
                            exame.codamb = codamb
                            exame.local = '112'
                            exame.descr = TabAmb.objects.filter(codamb=codamb).filter(codconvenio=codconvenio.hm).first().descr
                            exame.quant = '1'
                            exame.codmedico = codmedico
                            exame.usuario = API_USER
                            exame.datasist = datetime.now()
                            exame.chave = novo_codmov
                            exame.valor = TabAmb.objects.filter(codamb=codamb).filter(codconvenio=codconvenio.hm).first().ch
                            exame.tipo = 'R'
                            exame.dataproc = datetime.now()
                            exame.codpacref = codpac_sisac
                            novocodigo_exame = incrementa_codigoexame()
                            exame.codigo = novocodigo_exame
                            exame.save()

                    
                    # Se qtd realizada = quantidade prescrita, significa que paciente teve alta
                    # Então insere flag TRATADO = 'SIM' na prescrição e no planejamento do paciente.
                    # Paciente recebeu alta e um email é enviado informando.
                    if prescricao.naplicacoes == qtd_realizada:
                        prescricao.tratado = 'SIM'
                        prescricao.save()

                        for planej in planejamento:
                            planej.tratado = 'SIM'
                            planej.save()

                        prescrradio = PrescrRadio.objects.filter(numpresc=prescricao.numpresc)

                        for presc in prescrradio:
                            presc.tratado = 'SIM'
                            presc.save()
                        
                        print(f'[ATUALIZA_AGENDA] - Última sessão do paciente{str(codpac_sisac)}. {qtd_realizada} sessões realizadas. Inserida flag TRATADO=SIM para o tratamento do paciente.')
                        sendmail_alta_paciente(str(codpac_sisac.paciente))
                else:
                    print(f'[ATUALIZA_AGENDA] - Paciente {codpac_sisac} não atendeu aos critérios de execução de rotina. Verificar se possui possui prescrição, ou se possui planejamento.')
                i += 1
    print('[ATUALIZA_AGENDA] - Atualização da agenda concluída com sucesso.', i, 'pacientes foram confirmados na agenda de tratamento de radioterapia SISAC.')

    # Marca a hora final e calcula tempo total decorrido.
    horafinal = datetime.now()
    tempodecorrido = horafinal - horainicial
    print('[ATUALIZA_AGENDA] - Tempo total decorrido:', tempodecorrido)

    # Consulta na agenda de radioterapia do SISAC se possui algum paciente que não foi confirmado
    query_sisac2 = Agenda.objects.filter(datahora__year=date.today().year, datahora__month=date.today().month, 
                                            datahora__day=date.today().day).filter(~Q(confatd='S')).filter(tipo='RAD')

    # Se houver algum paciente não confirmado,
    # Itera sobre o resultado, adicionando os pacientes não tratados em uma lista    
    list = []
    if query_sisac2 is not None:
        for obj in query_sisac2.iterator():
            list.append(str(obj.codpaciente_id) + ' - ' + str(obj.codpaciente))
        print('[ATUALIZA_AGENDA] - ', str(len(list)), 'paciente(s) não confirmado(s):', str(list), ' Verifique se houve tratamento realizado para o(s) paciente(s) informado(s) em', date.today().strftime("%d/%m/%Y") + '.')


@shared_task
def atualiza_planej():
    # Localiza planejamentos no MOSAIQ que aprovados na data de hoje.
    # Não significa que geraram uma nova versão do tratamento
    # Pois para pacientes novos, a data de Criação é igual à data de Aprovação
    campos = TxField.objects.filter(version=0).filter(dose_campo__gt=0).filter(sanct_dt__year=date.today().year, sanct_dt__month=date.today().month, sanct_dt__day=date.today().day)
    # campos = TxField.objects.filter(version=0).filter(dose_campo__gt=0).filter(sanct_dt__year=date.today().year, sanct_dt__month__gte='09', sanct_dt__day__gte='01')

   # Inicializa um dicionário para as unidades de medida da energia do tratamento
    energia_unidade_dict = {
        '0': '',
        '1': 'KV',
        '2': 'MV',
        '3': 'MeV'
        }

    campos_antigos = TxField.objects.filter(version__gt=0).filter(dose_campo__gt=0).filter(sanct_dt__year=date.today().year, sanct_dt__month=date.today().month, sanct_dt__day=date.today().day)
    if campos_antigos is not None:
        for campo in campos_antigos:
            Planejfisico.objects.filter(id_mosaiq=campo.id_campo).delete()
            Planejfisicoc.objects.filter(id_mosaiq=campo.id_campo).delete()
            PrescrRadio.objects.filter(id_mosaiq=campo.id_campo).delete()

    i = 0
    for obj in campos.iterator():
        i += 1
        print('[ATUALIZA_PLANEJ] - iteração campo', i, obj)

        codpac_sisac = relaciona_paciente(obj.id_paciente)

        if codpac_sisac:
            print(f'[ATUALIZA_PLANEJ] - Paciente encontrado: {codpac_sisac}')
            prescricao = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last()
            if prescricao is not None:
                planejfisicoc = Planejfisicoc.objects.filter(codpaciente=codpac_sisac).filter(id_mosaiq=obj.id_campo).filter(ativo=1)

                if planejfisicoc.count() > 0:
                    print('[ATUALIZA_PLANEJ] - Planejamento encontrado para o paciente', codpac_sisac, 'numero do campo:', obj.numero_campo)
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
                        planej2.id_mosaiq = obj.id_campo
                        planej2.save()
                else:
                    print('[ATUALIZA_PLANEJ] - planejamento NÃO encontrado para o paciente', codpac_sisac, 'numero do campo', obj.numero_campo)
                    print('[ATUALIZA_PLANEJ] - gerando registro na tabela PlanejFisicoC')
                    novo_planejfisicoc = Planejfisicoc()
                    novo_planejfisicoc.codpaciente = codpac_sisac
                    novo_planejfisicoc.codmovimento = codpac_sisac.codpaciente
                    novo_planejfisicoc.numpresc = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().numpresc
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

                    # Realizada chamada na função inicio_tratamento(), passando como parâmetro o obj iterado no loop anterior
                    # Realiza a verificação para definir o início do tratamento.
                    iniciotrat = inicio_tratamento(obj)

                    novo_planejfisicoc.iniciotrat = iniciotrat
                    novo_planejfisicoc.incidencia = '3D'
                    novo_planejfisicoc.tpfeixe = obj.id_fase.modalidade
                    novo_planejfisicoc.fase = obj.id_fase.numerofase
                    novo_planejfisicoc.usuario = API_USER
                    novo_planejfisicoc.id_mosaiq = obj.id_campo
                    novo_planejfisicoc.id_fase_mosaiq = obj.id_fase_id
                    novo_planejfisicoc.save()

                planejfisico = Planejfisico.objects.filter(codpaciente=codpac_sisac).filter(id_mosaiq=obj.id_campo).filter(ativo=1)

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
                        planej.angulacao = 'G-' + str(obj.txfieldpoint_set.first().gantry) + ';M-' + str(obj.txfieldpoint_set.first().mesa) + ';C-' + str(obj.txfieldpoint_set.first().colimador)
                        planej.datasist = datetime.now()
                        planej.usuario = API_USER
                        planej.id_mosaiq = obj.id_campo
                        planej.save()
                else:            
                    novo_planejfisico = Planejfisico()
                    novo_planejfisico.idplanejfisicoc = Planejfisicoc.objects.filter(codpaciente=codpac_sisac).order_by('idplanejfisicoc').last()
                    novo_planejfisico.codpaciente = codpac_sisac
                    novo_planejfisico.codmovimento = codpac_sisac.codpaciente
                    novo_planejfisico.numpresc = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().numpresc
                    novo_planejfisico.incidencia = '3D'
                    novo_planejfisico.energia = str(obj.txfieldpoint_set.first().energia) + energia_unidade_dict[str(obj.txfieldpoint_set.first().energia_unidade)]
                    novo_planejfisico.tecnica = obj.id_fase.tecnica
                    novo_planejfisico.unidade_monitora = obj.unidade_monitora
                    novo_planejfisico.angulacao = 'G-' + str(obj.txfieldpoint_set.first().gantry) + ';M-' + str(obj.txfieldpoint_set.first().mesa) + ';C-' + str(obj.txfieldpoint_set.first().colimador)
                    novo_planejfisico.nplanejamento = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().ntratamento
                    novo_planejfisico.ntratamento = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().ntratamento
                    novo_planejfisico.ncampo = obj.numero_campo
                    novo_planejfisico.fase = obj.id_fase.numerofase
                    novo_planejfisico.ativo = 1
                    novo_planejfisico.datasist = datetime.now()
                    novo_planejfisico.dtt = obj.id_fase.dosetotal
                    novo_planejfisico.dtd = obj.dose_campo
                    novo_planejfisico.nomecampo = obj.nome_campo
                    novo_planejfisico.usuario = API_USER
                    novo_planejfisico.id_mosaiq = obj.id_campo 
                    novo_planejfisico.id_fase_mosaiq = obj.id_fase_id
                    novo_planejfisico.save()

                prescrradio = PrescrRadio.objects.filter(codpaciente=codpac_sisac).filter(numpresc=Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().numpresc).filter(tratado='NAO').filter(id_mosaiq=obj.id_campo)

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
                        presc.usuario = API_USER
                        presc.id_mosaiq = obj.id_campo
                        presc.save()
                else:
                    novapresc = PrescrRadio()
                    novapresc.ncampos = obj.numero_campo
                    novapresc.idradio = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().idradio
                    novapresc.codmovimento = codpac_sisac.codpaciente
                    novapresc.locanatomica = obj.id_fase.locanatomica
                    novapresc.datasist = datetime.now()
                    novapresc.numpresc = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().numpresc
                    novapresc.incidencia = '3D'
                    novapresc.naplicacoes = obj.id_fase.qtdsessoes
                    novapresc.ntratamento = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().ntratamento
                    novapresc.codpaciente = codpac_sisac
                    novapresc.usuario = API_USER
                    novapresc.energia = str(obj.txfieldpoint_set.first().energia) + energia_unidade_dict[str(obj.txfieldpoint_set.first().energia_unidade)]
                    novapresc.tecnica = obj.id_fase.tecnica
                    novapresc.tpfeixe = obj.id_fase.modalidade
                    novapresc.dosettotal = obj.id_fase.dosetotal
                    novapresc.dosetdiaria = obj.dose_campo
                    novapresc.fase = obj.id_fase.numerofase

                    # Realizada chamada na função inicio_tratamento(), passando como parâmetro o obj iterado no loop anterior
                    # Realiza a verificação para definir o início do tratamento.
                    iniciotrat = inicio_tratamento(obj)

                    print(f'[ATUALIZA_PLANEJ] - ID Fase: {obj.id_fase}, início trat: {iniciotrat}')
                    novapresc.iniciotrat = iniciotrat
                    novapresc.id_mosaiq = obj.id_campo
                    novapresc.id_fase_mosaiq = obj.id_fase_id
                    novapresc.save()

                primeira_agenda = Agenda.objects.filter(codpaciente=codpac_sisac).filter(tipo='RAD').filter(planejado='N').filter(confatd='N').order_by('idagenda').first()
                if primeira_agenda is not None:
                    primeira_agenda.planejado = 'S'            
                    primeira_agenda.save() 
                    print(f'[ATUALIZA_PLANEJ] - Alterado a agenda do paciente {codpac_sisac}, dia {primeira_agenda.datahora} com status Planejado OK.')
                else:
                    pass

        else:
            print(f'[ATUALIZA_PLANEJ] - Paciente {codpac_sisac} sem prescrição médica no SISAC')


@shared_task
def cria_agenda_radio():

    agenda_mosaiq_criada_hoje = Schedule.objects.filter(create_dt__year=date.today().year, create_dt__month=date.today().month, create_dt__day=date.today().day).filter(activity='3D').filter(version=0).filter(~Q(suppressed=1))

    novos_pacientes_agendados = []
    agendamento_existente = []

    for paciente in agenda_mosaiq_criada_hoje:
        if paciente.id_paciente not in novos_pacientes_agendados:
            novos_pacientes_agendados.append(paciente.id_paciente)

    for pac in novos_pacientes_agendados:
        codpac_sisac = relaciona_paciente(pac)
        if codpac_sisac:            
            primeira_agenda = Agenda.objects.filter(codpaciente=codpac_sisac).filter(obs__icontains='Sessão de Radioterapia').filter(planejado='S')
            if primeira_agenda.count() <= 1:
                # altera_primeira_agenda = primeira_agenda.first()
                # if altera_primeira_agenda is not None:
                #     altera_primeira_agenda.tipo = ''
                #     altera_primeira_agenda.tipooriginal = ''
                #     altera_primeira_agenda.save()
                agenda_mosaiq = Schedule.objects.filter(id_paciente=pac.id_paciente).filter(activity='3D').filter(~Q(suppressed=1))
                for agd in agenda_mosaiq:
                    print(f'[CRIA_AGENDA_RADIO] - Iniciando iterações para paciente {codpac_sisac}...')
                    checa_agenda = Agenda.objects.filter(datahora=agd.dataagenda).filter(obs__icontains='Sessão de Radioterapia')
                    if checa_agenda.count() > 0:
                        print(f'[CRIA_AGENDA_RADIO] - Já existe agendamento no dia {agd.dataagenda.strftime("%d/%m/%Y - %H:%M:%S")}.')
                        dict = {}
                        dict['IDAgenda_SISAC'] = checa_agenda.first().idagenda
                        dict['Paciente'] = str(checa_agenda.first().codpaciente.codpaciente) + ' - ' + str(checa_agenda.first().codpaciente.paciente)
                        dict['DataHora_Existente'] = checa_agenda.first().datahora.strftime("%d/%m/%Y - %H:%M:%S")
                        dict['Tentou_Encaixar'] = str(codpac_sisac.codpaciente) + ' - ' + str(codpac_sisac.paciente)
                        agendamento_existente.append(dict)
                    else:
                        print(f'[CRIA_AGENDA_RADIO] - Criando agenda para paciente {codpac_sisac}, dia {agd.dataagenda.strftime("%d/%m/%Y - %H:%M:%S")}')
                        agenda = Agenda()
                        agenda.codmedico = '103'
                        agenda.datahora = agd.dataagenda
                        agenda.nome = codpac_sisac.paciente
                        agenda.codconvenio = Entrada.objects.filter(codpaciente=codpac_sisac).filter(filial='01').order_by('datahoraent').last().codconvenio
                        agenda.codpaciente = codpac_sisac
                        agenda.obs = 'Sessão de Radioterapia'
                        agenda.usuario = API_USER
                        agenda.descr = Entrada.objects.filter(codpaciente=codpac_sisac).filter(filial='01').order_by('datahoraent').last().codconvenio.descr
                        agenda.datasist = datetime.now()
                        agenda.confatd = 'N'
                        agenda.tipo = 'RAD'
                        agenda.plano = Entrada.objects.filter(codpaciente=codpac_sisac).filter(filial='01').order_by('datahoraent').last().plano
                        agenda.telefone = codpac_sisac.telefone2
                        senha = senhanova()
                        agenda.senha = senha
                        agenda.ntratradio = Radioterapia.objects.filter(codpaciente=codpac_sisac).last().ntratamento
                        agenda.planejado = 'S'
                        agenda.whatsapp = codpac_sisac.whatsapp
                        agenda.tipooriginal = 'RAD'
                        agenda.save()

            else:
                print(f'[CRIA_AGENDA_RADIO] - Nada a fazer para o paciente {codpac_sisac}...')

    if len(agendamento_existente) > 0:
        msg = f'A tarefa de criação de agenda automática do SISAC reportou existência de agendamentos existentes. \nViolação de integridade foi evitada para o(s) seguinte(s) agendamento(s):{agendamento_existente}'
        sendmail_cria_agenda('Cria Agenda Radio SISAC', msg)
        print(f'[CRIA_AGENDA_RADIO] - {msg}')
    print(f'[CRIA_AGENDA_RADIO] - Tarefa concluída.')


@shared_task
def atualiza_agenda_sisac():

    # novos_pacientes_versionados = []
    # agenda_mosaiq_versionada_hoje = Schedule.objects.filter(edit_dt__year=date.today().year, edit_dt__month=date.today().month, edit_dt__day=date.today().day).filter(activity='3D').filter(version__gt=0)
    # if agenda_mosaiq_versionada_hoje is not None:
    #     for paciente in agenda_mosaiq_versionada_hoje:
    #         if paciente.id_paciente not in novos_pacientes_versionados:
    #             novos_pacientes_versionados.append(paciente.id_paciente)

    # for pac in novos_pacientes_versionados:
    #     codpac_sisac = Cadpaciente.objects.get(cpf=pac.cpf)
    #     if codpac_sisac is not None: 
    #         Agenda.objects.filter(codpaciente=codpac_sisac).filter(tipo='RAD').filter(~Q(confatd='S')).delete()

    agenda_mosaiq_editada_hoje = Schedule.objects.filter(edit_dt__year=date.today().year, edit_dt__month=date.today().month, edit_dt__day=date.today().day).filter(activity='3D').filter(version=0).filter(~Q(suppressed=1)).filter(~Q(status=' C'))

    novos_pacientes_agendados = []

    for paciente in agenda_mosaiq_editada_hoje:
        if paciente.id_paciente not in novos_pacientes_agendados:
            novos_pacientes_agendados.append(paciente.id_paciente)

    for pac in novos_pacientes_agendados:
        print(f'[ATUALIZA_AGENDA_SISAC] - Paciente {pac}, CPF {pac.cpf}')
        codpac_sisac = relaciona_paciente(pac)
        if codpac_sisac:
            agenda_mosaiq = Schedule.objects.filter(dataagenda__gte=date.today()).order_by('dataagenda').filter(id_paciente=pac.id_paciente).filter(activity='3D').filter(~Q(suppressed=1)).filter(~Q(status=' C'))
            for agd in agenda_mosaiq:
                agenda = Agenda.objects.filter(datahora=agd.dataagenda).filter(tipo='RAD').filter(planejado='S').first()
                if agenda is None:
                    agenda_sisac = Agenda.objects.filter(codpaciente=codpac_sisac).filter(datahora__year=agd.dataagenda.year, datahora__month=agd.dataagenda.month, datahora__day=agd.dataagenda.day).filter(tipo='RAD').first() 
                    if agenda_sisac is not None:
                        agenda_sisac.datahora = agd.dataagenda
                        agenda_sisac.save()
                        print(f'[ATUALIZA_AGENDA_SISAC] - Agenda do paciente {codpac_sisac} atualizada. Dia/hora anterior: {agenda_sisac.datahora.strftime("%d/%m/%Y - %H:%M:%S")}. Dia/hora atuaç: {agd.dataagenda}')                            
                else:
                    if agenda.codpaciente != codpac_sisac:                        
                        print(f'[ATUALIZA_AGENDA_SISAC] - Agendamento do dia {agenda.datahora.strftime("%d/%m/%Y - %H:%M:%S")} pertence ao paciente {agenda.codpaciente}. Inválido alterar para {codpac_sisac}')


@shared_task
def atualiza_planej_pac(pac):
    # Localiza planejamentos no MOSAIQ que aprovados na data de hoje.
    # Não significa que geraram uma nova versão do tratamento
    # Pois para pacientes novos, a data de Criação é igual à data de Aprovação
    campos = TxField.objects.filter(version=0).filter(dose_campo__gt=0).filter(id_paciente=pac)

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

        pac_mosaiq = Patient.objects.get(id_paciente=pac)
        codpac_sisac = relaciona_paciente(pac_mosaiq)

        if codpac_sisac is not None:
            print('paciente encontrado')
            planejfisicoc = Planejfisicoc.objects.filter(codpaciente=codpac_sisac).filter(id_mosaiq=obj.id_campo).filter(ativo=1)

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
                    planej2.id_mosaiq = obj.id_campo
                    planej2.save()
            else:
                print('planejamento NÃO encontrado para o paciente', codpac_sisac, 'numero do campo', obj.numero_campo)
                print('gerando registro na tabela PlanejFisicoC')
                print(obj)
                novo_planejfisicoc = Planejfisicoc()
                novo_planejfisicoc.codpaciente = codpac_sisac
                novo_planejfisicoc.codmovimento = codpac_sisac.codpaciente
                novo_planejfisicoc.numpresc = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().numpresc
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
                iniciotrat = inicio_tratamento(obj)

                print(obj.id_fase, iniciotrat)
                novo_planejfisicoc.iniciotrat = iniciotrat
                novo_planejfisicoc.incidencia = '3D'
                novo_planejfisicoc.tpfeixe = obj.id_fase.modalidade
                novo_planejfisicoc.fase = obj.id_fase.numerofase
                novo_planejfisicoc.usuario = API_USER
                novo_planejfisicoc.id_mosaiq = obj.id_campo
                novo_planejfisicoc.save()

            planejfisico = Planejfisico.objects.filter(codpaciente=codpac_sisac).filter(id_mosaiq=obj.id_campo).filter(ativo=1)

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
                    planej.angulacao = 'G-' + str(obj.txfieldpoint_set.first().gantry) + ';M-' + str(obj.txfieldpoint_set.first().mesa) + ';C-' + str(obj.txfieldpoint_set.first().colimador)
                    planej.id_mosaiq = obj.id_campo
                    planej.save()
            else:
                novo_planejfisico = Planejfisico()
                novo_planejfisico.idplanejfisicoc = Planejfisicoc.objects.filter(codpaciente=codpac_sisac).order_by('idplanejfisicoc').last()
                novo_planejfisico.codpaciente = codpac_sisac
                novo_planejfisico.codmovimento = codpac_sisac.codpaciente
                novo_planejfisico.numpresc = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().numpresc
                novo_planejfisico.incidencia = '3D'
                novo_planejfisico.energia = str(obj.txfieldpoint_set.first().energia) + energia_unidade_dict[str(obj.txfieldpoint_set.first().energia_unidade)]
                novo_planejfisico.tecnica = obj.id_fase.tecnica
                novo_planejfisico.unidade_monitora = obj.unidade_monitora
                novo_planejfisico.angulacao = 'G-' + str(obj.txfieldpoint_set.first().gantry) + ';M-' + str(obj.txfieldpoint_set.first().mesa) + ';C-' + str(obj.txfieldpoint_set.first().colimador)
                novo_planejfisico.nplanejamento = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().ntratamento
                novo_planejfisico.ntratamento = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().ntratamento
                novo_planejfisico.ncampo = obj.numero_campo
                novo_planejfisico.fase = obj.id_fase.numerofase
                novo_planejfisico.ativo = 1
                novo_planejfisico.datasist = datetime.now()
                novo_planejfisico.dtt = obj.id_fase.dosetotal
                novo_planejfisico.dtd = obj.dose_campo
                novo_planejfisico.nomecampo = obj.nome_campo
                novo_planejfisico.usuario = API_USER
                novo_planejfisico.id_mosaiq = obj.id_campo
                novo_planejfisico.save()

            prescrradio = PrescrRadio.objects.filter(codpaciente=codpac_sisac).filter(numpresc=Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().numpresc).filter(tratado='NAO').filter(id_mosaiq=obj.id_campo)

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
                    presc.usuario = API_USER
                    presc.id_mosaiq = obj.id_campo
                    presc.save()
            else:
                novapresc = PrescrRadio()
                novapresc.ncampos = obj.numero_campo
                novapresc.idradio = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().idradio
                novapresc.codmovimento = codpac_sisac.codpaciente
                novapresc.locanatomica = obj.id_fase.locanatomica
                novapresc.datasist = datetime.now()
                novapresc.numpresc = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().numpresc
                novapresc.incidencia = '3D'
                novapresc.naplicacoes = obj.id_fase.qtdsessoes
                novapresc.ntratamento = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last().ntratamento
                novapresc.codpaciente = codpac_sisac
                novapresc.usuario = API_USER
                novapresc.energia = str(obj.txfieldpoint_set.first().energia) + energia_unidade_dict[str(obj.txfieldpoint_set.first().energia_unidade)]
                novapresc.tecnica = obj.id_fase.tecnica
                novapresc.tpfeixe = obj.id_fase.modalidade
                novapresc.dosettotal = obj.id_fase.dosetotal
                novapresc.dosetdiaria = obj.dose_campo
                novapresc.fase = obj.id_fase.numerofase

                # Verifica se a fase está relacionada com outra para definir o início do tratamento
                # Se não houver fase relacionada, inicio tratamento = 1
                # Se houver, define início tratamento com o valor obtido da coluna Reference_Fraction, tabela Fase
                iniciotrat = inicio_tratamento(obj)

                novapresc.iniciotrat = iniciotrat
                novapresc.id_mosaiq = obj.id_campo
                novapresc.save()

            primeira_agenda = Agenda.objects.filter(codpaciente=codpac_sisac).filter(tipo='RAD').filter(planejado='N').filter(confatd='N').order_by('idagenda').first()
            if primeira_agenda is not None:
                primeira_agenda.planejado = 'S'            
                primeira_agenda.save() 
                print(f'Alterado a agenda do paciente {codpac_sisac}, dia {primeira_agenda.datahora} com status Planejado OK.')
            else:
                print('Não Identificado')


def alta():
    prescricoes_alta = Radioterapia.objects.filter(tratado='SIM')
    for prescricao in prescricoes_alta:
        planejfisico = Planejfisico.objects.filter(numpresc=prescricao)
        if planejfisico is not None:
            for planej in planejfisico:
                planej.tratado = 'SIM'
                planej.save()
                print(f'Flag TRATADO SIM inserida para o campo {planej}, paciente {planej.codpaciente}')
        prescrradio = PrescrRadio.objects.filter(numpresc=prescricao)
        if prescrradio is not None:
            for presc in prescrradio:
                presc.tratado = 'SIM'
                presc.save()
                print(f'Flag TRATADO SIM inserida para o campo {presc}, paciente {presc.codpaciente}')


def inserepacote(pac):
    codpac_sisac = Cadpaciente.objects.get(codpaciente=pac)

    def addcodmovimento(codmovimento):
        cut = codmovimento.split('.')
        seqadd = int(cut[1]) + 1
        if seqadd < 10:
            seqadd = '0' + str(seqadd)
        codfinal = cut[0] + '.' + str(seqadd)  

        return codfinal
    
    def incrementa_codigoexame():
        prm_exame = TAB_Parametro.objects.get(prm_nome='TAB_EXAME')
        novo_codigo = prm_exame.prm_sequencia + 1
        prm_exame.prm_sequencia = novo_codigo
        prm_exame.save()

        return novo_codigo

    def incrementa_natendimento():
        prm_exame = TAB_Parametro.objects.get(prm_nome='TAB_ATENDIMENTO')
        novo_codigo = prm_exame.prm_sequencia + 1
        prm_exame.prm_sequencia = novo_codigo
        prm_exame.save()

        return novo_codigo


    prescricao = Radioterapia.objects.filter(codpaciente=codpac_sisac).order_by('numpresc').last()
    print(f'Primeira sessão de radioterapia do paciente {codpac_sisac}. Iniciando lançamento do pacote do tratamento na conta do paciente...')
    codamb = SolicExa.objects.filter(npresc=prescricao.numpresc).order_by('item').first().codamb
    primeira_entrada = Entrada.objects.filter(codpaciente=codpac_sisac).order_by('datahoraent').first()
    codconvenio = primeira_entrada.codconvenio
    matricula = primeira_entrada.matricula
    codmedico = primeira_entrada.codmedico
    plano = primeira_entrada.plano
    ultimo_codmov = Entrada.objects.filter(codpaciente=codpac_sisac).order_by('datahoraent').last()
    novo_codmov = addcodmovimento(str(ultimo_codmov))
    
    # Gerar registro do pacote de tratamento na tabela Entrada
    entrada = Entrada()
    entrada.codmovimento = novo_codmov
    entrada.codpaciente = codpac_sisac
    entrada.codconvenio = codconvenio
    entrada.matricula = matricula
    entrada.tipo = '4'
    entrada.datahoraent = datetime.now()
    entrada.hist = TabAmb.objects.filter(codamb=codamb).filter(codconvenio=codconvenio.hm).first().descr
    entrada.codmedico = codmedico
    entrada.local = '112'
    entrada.recep = API_USER
    entrada.total = TabAmb.objects.filter(codamb=codamb).filter(codconvenio=codconvenio.hm).first().ch
    entrada.fechado = 'P'
    entrada.codamb = codamb
    entrada.datasist = datetime.now()
    entrada.plano = plano
    entrada.tabhm = CadConvenio.objects.get(codconvenio=codconvenio).hm
    entrada.datahoraint = datetime.now()
    entrada.localini = '112'
    novocodigo_natendimento = incrementa_natendimento()
    entrada.natendimento = novocodigo_natendimento
    entrada.datamarcada = datetime.now()
    entrada.save()

    # Gerar registro do pacote de tratamento na tabela Fatura
    fatura = Fatura()
    fatura.codpaciente = novo_codmov
    fatura.grupo = '1'
    fatura.codtaxa = codamb
    fatura.descr = TabAmb.objects.filter(codamb=codamb).filter(codconvenio=codconvenio.hm).first().descr
    fatura.data = datetime.now()
    fatura.valor = TabAmb.objects.filter(codamb=codamb).filter(codconvenio=codconvenio.hm).first().ch
    fatura.quant = '1'
    fatura.filme = '0'
    fatura.codmedico = codmedico
    fatura.datasist = datetime.now()
    fatura.usuario = API_USER
    fatura.codamb = codamb
    fatura.ch = TabAmb.objects.filter(codamb=codamb).filter(codconvenio=codconvenio.hm).first().ch
    fatura.local = '112'
    fatura.honor = TabAmb.objects.filter(codamb=codamb).filter(codconvenio=codconvenio.hm).first().ch
    fatura.vpprof = TabAmb.objects.filter(codamb=codamb).filter(codconvenio=codconvenio.hm).first().ch
    fatura.obs = f'Tab.Honor {CadConvenio.objects.get(codconvenio=codconvenio).hm} {CadConvenio.objects.get(codconvenio=CadConvenio.objects.get(codconvenio=codconvenio).hm).descr}'
    fatura.localac = '112'
    fatura.save()

    # Gerar registro do pacote de tratamento na tabela Exame
    exame = Exame()
    exame.codpaciente = novo_codmov
    exame.codamb = codamb
    exame.local = '112'
    exame.descr = TabAmb.objects.filter(codamb=codamb).filter(codconvenio=codconvenio.hm).first().descr
    exame.quant = '1'
    exame.codmedico = codmedico
    exame.usuario = API_USER
    exame.datasist = datetime.now()
    exame.chave = novo_codmov
    exame.valor = TabAmb.objects.filter(codamb=codamb).filter(codconvenio=codconvenio.hm).first().ch
    exame.tipo = 'R'
    exame.dataproc = datetime.now()
    exame.codpacref = codpac_sisac
    novocodigo_exame = incrementa_codigoexame()
    exame.codigo = novocodigo_exame
    exame.save()


def cria_agenda_radio2(pac):

    agenda_mosaiq_criada_hoje = Schedule.objects.filter(id_paciente=pac).filter(version=0).filter(~Q(suppressed=1))

    novos_pacientes_agendados = []
    agendamento_existente = []

    for paciente in agenda_mosaiq_criada_hoje:
        if paciente.id_paciente not in novos_pacientes_agendados:
            novos_pacientes_agendados.append(paciente.id_paciente)

    for pac in novos_pacientes_agendados:
        codpac_sisac = relaciona_paciente(pac)
        if codpac_sisac:            
            primeira_agenda = Agenda.objects.filter(codpaciente=codpac_sisac).filter(tipo='RAD').filter(planejado='S')
            if primeira_agenda.count() <= 1:
                # altera_primeira_agenda = primeira_agenda.first()
                # if altera_primeira_agenda is not None:
                #     altera_primeira_agenda.tipo = ''
                #     altera_primeira_agenda.tipooriginal = ''
                #     altera_primeira_agenda.save()
                agenda_mosaiq = Schedule.objects.filter(id_paciente=pac.id_paciente).filter(activity='3D').filter(~Q(suppressed=1))
                for agd in agenda_mosaiq:
                    print(f'Iniciando iterações para paciente {codpac_sisac}...')
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
                        print(f'Criando agenda para paciente {codpac_sisac}, dia {agd.dataagenda.strftime("%d/%m/%Y - %H:%M:%S")}')
                        agenda = Agenda()
                        agenda.codmedico = '103'
                        agenda.datahora = agd.dataagenda
                        agenda.nome = codpac_sisac.paciente
                        agenda.codconvenio = Entrada.objects.filter(codpaciente=codpac_sisac).order_by('datahoraent').last().codconvenio
                        agenda.codpaciente = codpac_sisac
                        agenda.obs = 'Sessão de Radioterapia'
                        agenda.usuario = API_USER
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

            else:
                print(f'Nada a fazer para o paciente {codpac_sisac}...')

    if len(agendamento_existente) > 0:
        msg = f'A tarefa de criação de agenda automática do SISAC reportou existência de agendamentos existentes. \nViolação de integridade foi evitada para o(s) seguinte(s) agendamento(s):{agendamento_existente}'
        sendmail_cria_agenda('Cria Agenda Radio SISAC', msg)
    print(f'Tarefa concluída.')


def entrada(pac):
    codpac_sisac = Cadpaciente.objects.get(codpaciente=pac)

    def addcodmovimento(codmovimento):
        cut = codmovimento.split('.')
        seqadd = int(cut[1]) + 1
        if seqadd < 10:
            seqadd = '0' + str(seqadd)
        codfinal = cut[0] + '.' + str(seqadd)  

        return codfinal
    
    def incrementa_natendimento():
        prm_exame = TAB_Parametro.objects.get(prm_nome='TAB_ATENDIMENTO')
        novo_codigo = prm_exame.prm_sequencia + 1
        prm_exame.prm_sequencia = novo_codigo
        prm_exame.save()

        return novo_codigo


    ultimo_codmov = Entrada.objects.filter(codpaciente=codpac_sisac).order_by('datahoraent').last()
    novo_codmov = addcodmovimento(str(ultimo_codmov))
    
    # Gerar registro do pacote de tratamento na tabela Entrada
    entrada = Entrada()
    entrada.codmovimento = novo_codmov
    entrada.codpaciente = codpac_sisac
    entrada.codconvenio = CadConvenio.objects.first()
    entrada.matricula = ''
    entrada.tipo = '4'
    entrada.datahoraent = datetime.now()
    entrada.hist = ''
    entrada.codmedico = '001'
    entrada.local = '112'
    entrada.recep = API_USER
    entrada.total = 0
    entrada.fechado = 'P'
    entrada.codamb = ''
    entrada.datasist = datetime.now()
    entrada.plano = ''
    entrada.tabhm = '001'
    entrada.datahoraint = datetime.now()
    entrada.localini = '112'
    novocodigo_natendimento = incrementa_natendimento()
    entrada.natendimento = novocodigo_natendimento
    entrada.datamarcada = datetime.now()
    entrada.save()

