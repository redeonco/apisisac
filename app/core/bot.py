from core.functions import *
import os
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
from telegram.ext import Updater



# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)

# logger = logging.getLogger(__name__)

NOME, ASSUNTO, CHAMADO, CREDENCIAIS, EMAIL, SENHA, ENVIAR, SAIR = range(8)

def start(update: Update, context: CallbackContext):
    global user
    user = relaciona_usuario(update.message.from_user)
    if user:
        reply_keyboard = [['Abrir Chamado']]
        update.message.reply_text(f'Olá, {user.first_name}!\nQue bom tê-lo de volta.\U0001F929\n\n\nO que deseja fazer?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Abrir Chamado?')
        )
        return ASSUNTO
    else:
        update.message.reply_text('Olá! Me chamo Jarvis \U0001F916, o bot da TI. \U0001F601'
        '\n\nDarei o meu melhor para ajudar você. \U0001F929'
        '\nAntes de começarmos, qual seu nome completo?'
        )

        return NOME


def nome(update: Update, context: CallbackContext):    
    # logger.info("Gender of %s: %s", user.first_name, update.message.text)

    reply_keyboard = [['Abrir Chamado', 'Não sei...']]

    global nomecompleto
    nomecompleto = update.message.text.strip().title()

    update.message.reply_text(
        f'Bonito nome, {nomecompleto.split()[0]}. '
        '\n\nO que deseja fazer?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Abrir Chamado?'
        ),
    )

    return ASSUNTO
    

def assunto(update: Update, context: CallbackContext):
    # logger.info("Gender of %s: %s", user.first_name, update.message.text)
    global user
    user = relaciona_usuario(update.message.from_user)
    reply_keyboard = [[
        'SISAC - Cancelar Entrada',
        'SISAC - Cancelar Alta',
        'SISAC - Acomodar Paciente',
        'SISAC - Desacomodar Paciente',
        'SISAC - Vincular Prescrição',
        'Suporte - Impressora',
        'Suporte - Computador',
        'Suporte - Internet',
        'Suporte - Email',
        'Suporte - Ramal',
        'Suporte - Biometria'
    ]]
    update.message.reply_text(f'Vamos lá, {user.first_name}. \nQual é o assunto? \n\nDica: tente usar palavras chaves, por exemplo: \n\nImpressora sem funcionar\n\nOu algo como:\nCancelar Entrada SISAC',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        ))

    return CHAMADO
    

def chamado(update: Update, context: CallbackContext):    
    # logger.info("Gender of %s: %s", user.first_name, update.message.text)
    global email_assunto
    email_assunto = update.message.text
    print(user.email)
    update.message.reply_text(f'Email: {user.email} Entendi.\nEm uma única mensagem, descreva detalhadamente o que está acontecendo. \U0001F58B')

    return CREDENCIAIS
    

def credenciais(update: Update, context: CallbackContext):
    global descricao_chamado
    descricao_chamado = update.message.text
    usuario = relaciona_usuario(update.message.from_user)
    if usuario.email:
        update.message.reply_text(f'Obrigado, {user.first_name}. Estamos quase no final. \nDigite sua senha de email por favor.')
        return SENHA
    else:         
        update.message.reply_text(f'Obrigado, {user.first_name}. \nPor favor, digite seu endereço de email.')

        return EMAIL


def emaill(update: Update, context: CallbackContext):
    user = update.message.from_user
    global email_endereco
    email_endereco = update.message.text
    adicionar_email(user, email_endereco)
    update.message.reply_text(f'Estamos quase no final.\nPreciso agora que digite sua senha.')

    return SENHA


def senha(update: Update, context: CallbackContext):
    reply_keyboard = [['Ok']]
    global email_senha
    email_senha = update.message.text
    update.message.reply_text(f'Estou preparando seu chamado, {user.first_name}... \U0001F4BB',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Ok'))

    if enviar_email(descricao_chamado, email_assunto, user.email.lower().strip(), email_senha.strip()):
        pass
    else:
        update.message.reply_text(f'Infelizmente não consegui enviar seu email utilizando a senha {email_senha}. \U0001F61E')
        return EMAIL

    return ENVIAR


def enviar(update: Update, context: CallbackContext):

    update.message.reply_text(f'Obrigado! \U0001F4E7 \nSeu chamado será aberto com os seguintes detalhes: \n\nEmail: {user.email} \nAssunto: {email_assunto}\nDescrição: {descricao_chamado} \n\nClique em /sair para encerrar a conversa.')

    print (f'Email: {user.email}. Senha: {email_senha}')

    
    return SAIR


def sair(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    # logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        f'Tchau, {user.first_name} \U0001F9BE. \nEspero que a gente volte a conversar qualquer dia desses... \U0001F44B \n\nPara inciar uma nova conversa, \nClique em /start \U0001F919 \n\nAté breve! \U0001F91D'
    )

    return ConversationHandler.END


def main() -> None:
    updater = Updater(os.environ.get('TELEGRAM_BOT_TOKEN'))

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NOME: [MessageHandler(Filters.text, nome)],
            ASSUNTO: [MessageHandler(Filters.text, assunto)],
            CHAMADO: [MessageHandler(Filters.text, chamado)],
            CREDENCIAIS: [MessageHandler(Filters.text, credenciais)],
            EMAIL: [MessageHandler(Filters.text, emaill)],
            SENHA: [MessageHandler(Filters.text, senha)],
            ENVIAR: [MessageHandler(Filters.text, enviar)],
            SAIR: [CommandHandler('sair', sair)]

        },
        fallbacks=[CommandHandler('sair', sair)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
     main()
