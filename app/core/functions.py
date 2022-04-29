from core.models import *
from mosaiq_app.models import *
from control.models import *
from config.models import *
from datetime import date, datetime
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
import smtplib
from celery import shared_task
from smtplib import SMTPAuthenticationError
from .logger import API_LOGGER


"""
Conjunto de funções públicas utilizadas pelas rotinas do arquivo tasks.py
Escrevendo aqui funções utilizadas repetidamentes com o objetivo de melhorar
a estética e eficiência do código.
"""


def lista_emails():
    """
    Função utilizada para retornar uma lista com todos os emails cadastrados no Model EmailDestinatario
    """
    return [obj.email for obj in EmailDestinatario.objects.all()]


@shared_task
def sendmail_teste():
    """
    Função para enviar email. Recebe 2 parâmetros: nome da tarefa que a executou e uma mensagem do tipo string.
    """
    send_mail(
        'Núcleo de Sistemas - Relatório API - SISAC',
        'Email de teste',
        'chamado@oncoradium.com.br',
        lista_emails(),
        fail_silently=False,
    )


@shared_task
def sendmail(qtdconfirmado, data):
    """
    Função para enviar email com a quantidade de pacientes confirmados em determinada data.
    Recebe 2 parâmetros: 
    *qtdconfirmado -> tipo numérico
    *data -> objeto datetime
    """
    try:
        send_mail(
            'Núcleo de Sistemas - Relatório API - SISAC',
            'Núcleo de Sistemas - Relatório API - SISAC. \n Olá. Segue resumo da execução da tarefa Atualiza Agenda, em ' + data.strftime("%d/%m/%Y às %H:%M:%S") +
            '.\nQuantidade de pacientes confirmados na agenda do SISAC: ' +
            str(qtdconfirmado) + '.',
            'chamado@oncoradium.com.br',
            lista_emails(),
            fail_silently=False,
        )
    except SMTPAuthenticationError:
        API_LOGGER.error(f'[SENDMAIL] - Falha de autenticação com o servidor SMTP :(')


@shared_task
def sendmail_cria_agenda(tarefa, msg):
    """
    Função para enviar email caso haja alguma mensagem de retorno da tarefa cria_agenda_radio
    Recebe 2 parâmetros do tipo string.
    """
    try:
        send_mail(
            'Núcleo de Sistemas - Relatório API - SISAC',
            'Núcleo de Sistemas - Relatório API - SISAC. \n Olá. Segue resumo da execução da tarefa ' + tarefa + ', em ' + datetime.now().strftime("%d/%m/%Y às %H:%M:%S") +
            '.\nA tarefa retornou a seguinte resposta: ' + msg + '.',
            'chamado@oncoradium.com.br',
            lista_emails(),
            fail_silently=False,
        )
    except SMTPAuthenticationError:
        API_LOGGER.error(f'[SENDMAIL_CRIA_AGENDA] - Falha de autenticação com o servidor SMTP :(')


def sendmail_generic_task(tarefa, msg):
    try:
        send_mail(
            'Núcleo de Sistemas - Relatório API - SISAC',
            'Núcleo de Sistemas - Relatório API - SISAC. \n Olá. Segue resumo da execução da tarefa ' + tarefa + ', em ' + datetime.now().strftime("%d/%m/%Y às %H:%M:%S") +
            '.\nA tarefa retornou a seguinte resposta: ' + msg + '.',
            'chamado@oncoradium.com.br',
            lista_emails(),
            fail_silently=False,
        )
    except SMTPAuthenticationError:
        API_LOGGER.error(f'[SENDMAIL_CRIA_AGENDA] - Falha de autenticação com o servidor SMTP :(')


@shared_task
def sendmail_alta_paciente(pac):
    """
    Função para enviar email notificando alta de paciente da radioterapia.
    Recebe um parâmetro do tipo string com o nome do paciente.
    """
    try:
        send_mail(
            'Relatório API - SISAC - Alta de Paciente',
            'Núcleo de Sistemas - Relatório API - SISAC. \n Olá. Última sessão de radioterapia realizada para o paciente' +
            pac + ', em ' + datetime.now().strftime("%d/%m/%Y às %H:%M:%S"),
            'chamado@oncoradium.com.br',
            ['ti@oncoradium.com.br', 'iara.souza@oncoradium.com.br'],
            fail_silently=False,
        )
    except SMTPAuthenticationError:
        API_LOGGER.error(f'[SENDMAIL_ALTA_PACIENTE] - Falha de autenticação com o servidor SMTP :(')


def addcodmovimento(codmovimento):
    """
    Função utilizada para incrementar sequencial do código movimento do paciente.
    A função recebe um parâmetro do tipo string no formato 'XXXXXX.YY'.
    Onde XXXXXX é o número do prontuário no SISAC, e YY é a sequência do movimento.
    Por exemplo: se receber '006049.10', irá retornar '006049.11'
    """
    cut = codmovimento.split('.')
    seqadd = int(cut[1]) + 1
    if seqadd < 10:
        seqadd = '0' + str(seqadd)
    codfinal = cut[0] + '.' + str(seqadd)
    return codfinal


def incrementa_codigoexame():
    """
    # Função utilizada para incremetar numeração CódigoExame, útil para a tabela Exame do SISAC
    # A função não recebe parâmetros.
    # Quando é chamada, a função faz leitura do valor na coluna PRM_Sequencia, tabela TAB_Parametro do banco CONFIG do SISAC.
    # Realiza incremento no valor obtido, atualiza o novo registro na tabela e retorna o novo valor incrementado.
    # O retorno da função é um valor do tipo inteiro.
    """
    prm_exame = TAB_Parametro.objects.get(prm_nome='TAB_EXAME')
    novo_codigo = prm_exame.prm_sequencia + 1
    prm_exame.prm_sequencia = novo_codigo
    prm_exame.save()

    return novo_codigo


def incrementa_natendimento():
    """
    Função utilizada para incremetar numeração NúmeroAtendimento, útil para a tabela Entrada do SISAC
    A função não recebe parâmetros.
    Quando é chamada, a função faz leitura do valor na coluna PRM_Sequencia, tabela TAB_Parametro do banco CONFIG do SISAC.
    Realiza incremento no valor obtido, atualiza o novo registro na tabela e retorna o novo valor incrementado.
    O retorno da função é um valor do tipo inteiro.
    """
    prm_exame = TAB_Parametro.objects.get(prm_nome='TAB_ATENDIMENTO')
    novo_codigo = prm_exame.prm_sequencia + 1
    prm_exame.prm_sequencia = novo_codigo
    prm_exame.save()

    return novo_codigo


def senhanova():
    """
    Função utilizada para incremetar numeração SenhaAgenda, útil para a tabela Agenda do SISAC
    A função não recebe parâmetros.
    Quando é chamada, a função faz leitura do valor na coluna PRM_Sequencia, tabela TAB_Parametro do banco CONFIG do SISAC.
    Realiza incremento no valor obtido, atualiza o novo registro na tabela e retorna o novo valor incrementado.
    O retorno da função é um valor do tipo string.
    """
    ultimasenha = TAB_Parametro.objects.get(prm_nome='SENHAAGENDA')  # 0006001
    ultimasenha.prm_sequencia = ultimasenha.prm_sequencia + 1
    ultimasenha.save()
    zeros = 7 - len(str(ultimasenha.prm_sequencia))
    senhafinal = '0' * zeros + str(ultimasenha.prm_sequencia)

    return senhafinal


def relaciona_paciente(id_paciente: Patient.id_paciente) -> Cadpaciente:
    """
    id_paciente = Patient.objects.get(id_paciente=pat_id1)

    Busca registro do paciente MOSAIQ no banco Controle para encontrar correspondência no SISAC
    Se não encontrar nenhum registro na tabela ControlPacientes com o ID MOSAIQ,
    A função irá iniciar o procedimento de relacionamento do paciente.
    Vai buscar no banco de dados do SISAC um paciente com o mesmo número de prontuário informado no MOSAIQ
    Se encontrar com o mesmo prontuário, verifica se o CPF é igual.
    Se o CPF corresponder, a função vai instanciar um objeto ControlPacientes e gravar o relacionamento

    Se encontrar registro na tabela ControlPacientes com o ID MOSAIQ, significa que já houve relacionamento anterior
    A função irá retornar um objeto da classe CadPaciente SISAC.    
    Se a função não encontrar nenhum relacionamento, irá sempre retornar False
    """
    try:

        try:
            busca = ControlPacientes.objects.get(
                id_paciente_mosaiq=id_paciente.pk)
            codpac_sisac = Cadpaciente.objects.get(
                codpaciente=busca.codpac_sisac)
            return codpac_sisac
        except:
            try:
                codpac_sisac = Cadpaciente.objects.exclude(
                    cpf='').get(codpaciente=id_paciente.codpac_sisac)
                if codpac_sisac.cpf == id_paciente.cpf.replace('.', '').replace('-', '').strip():
                    control_paciente = ControlPacientes()
                    control_paciente.id_paciente_mosaiq = id_paciente.pk
                    control_paciente.codpac_sisac = codpac_sisac.codpaciente
                    control_paciente.cpf = codpac_sisac.cpf
                    control_paciente.save()
                    return codpac_sisac
                else:
                    msg = f'Código do prontuário do paciente {id_paciente} no MOSAIQ é igual no SISAC, mas CPF não corresponde. \nCPF no MOSAIQ: {id_paciente.cpf}. CPF no SISAC: {codpac_sisac.cpf}'
                    sendmail_generic_task('Relaciona Paciente', msg)
                    API_LOGGER.warning(msg)
                    return False

            except:
                try:
                    codpac_sisac = Cadpaciente.objects.exclude(cpf='').get(
                        cpf=id_paciente.cpf.replace('.', '').replace('-', '').strip())
                    msg = f'Paciente {id_paciente} com número de prontuário digergente. \nProntuário MOSAIQ {id_paciente.codpac_sisac}. Prontuário SISAC {codpac_sisac.codpaciente}'
                    sendmail_generic_task('Relaciona paciente', msg)
                    API_LOGGER.warning(msg)
                    return codpac_sisac
                except:
                    msg = f'Nenhum relacionamento encontrado para o paciente {id_paciente}. Nem código do prontário nem CPF correspondem.'
                    sendmail_generic_task('Relaciona paciente', msg)
                    API_LOGGER.warning(msg)
                    return False

    except:
        API_LOGGER.error(f'Nenhum paciente MOSAIQ encontrado com o ID {id_paciente}')
        return False


def checafase(fase):
    """
    Função para verificar se a fase inicia ao mesmo tempo que outra
    A função verifica se existe um objeto relacionado na tabela fase
    Na coluna reference_sit_set_id. Este coluna aponta para ID de outra fase
    Indicando que as duas estão relacionadas.
    Se este for o caso, a coluna Reference_Fraction determina o número da sessão de início desta fase, relacionada à outra
    E a função retornará o ID da fase relacionada
    Se ocorrer a exceção ObjectDoesNotExist, a função retornará False
    """
    try:
        fase.reference_sit_set_id
        return fase.reference_sit_set_id
    except ObjectDoesNotExist:
        API_LOGGER.error('Não foi possível encontrar fase de referência para este tratamento no MOSAIQ')
        return False


def inicio_tratamento(obj):
    """
    Função utilizada para definir início do tratamento.
    Recebe como parâmetro um objeto da classe TxField do MOSAIQ.
    A função que verifica se a fase do campo está relacionada com outra para definir o início do tratamento
    Se não houver fase relacionada, inicio tratamento = 1
    Se houver, define início tratamento com o valor obtido da coluna Reference_Fraction, tabela Fase
    A função retorna um valor do tipo inteiro.
    """
    lista_fases = []
    if checafase(obj.id_fase) == False:
        fases = Fase.objects.filter(id_paciente=obj.id_paciente).filter(
            reference_sit_set_id__isnull=True)
        nfase = 0
        contador = 0
        for fase in fases:
            dict = {}
            nfase += 1
            dict['IDFase'] = fase
            dict['NumeroFase'] = nfase
            dict['QtdSessoes'] = fase.qtdsessoes
            if contador == 0:
                dict['InicioTrat'] = 1
            else:
                iniciotrat = lista_fases[contador-1]['InicioTrat'] + \
                    lista_fases[contador-1]['QtdSessoes']
                dict['InicioTrat'] = iniciotrat
            lista_fases.append(dict)
            contador += 1
        iniciotrat = list(filter(
            lambda lista_fases: lista_fases['IDFase'] == obj.id_fase, lista_fases))[0]['InicioTrat']

    else:
        iniciotrat = obj.id_fase.reference_fraction

    return iniciotrat


def relaciona_usuario(from_user):
    try:
        user = Usuarios.objects.get(user_id=from_user['id'])
        return user
    except Usuarios.DoesNotExist:
        user = Usuarios()
        user.username = from_user['username']
        user.first_name = from_user['first_name']
        user.last_name = from_user['last_name']
        user.user_id = from_user['id']
        user.save()
        return False


def adicionar_email(from_user, email):
    try:
        user = Usuarios.objects.get(user_id=from_user['id'])
        user.email = email
        user.save()
        return True
    except Usuarios.DoesNotExist:
        return False


def enviar_email(msg, assunto, user, senha):
    mail_from = user
    mail_subject = assunto
    mail_message_body = str(msg)
    mail_message = f'Descrição chamado: {mail_message_body}'
    final = 'Subject: {}\n\n{}'.format(mail_subject, mail_message)
    server = smtplib.SMTP('smtp-cluster.idc2.mandic.com.br', 587)
    try:
        server.login(mail_from, senha)
        server.sendmail(
            from_addr=mail_from, to_addrs='chamado@oncoradium.com.br', msg=final.encode('latin-1'))
        server.quit()
        return True
    except smtplib.SMTPAuthenticationError:
        return False
