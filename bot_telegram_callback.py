import telegram
import db_controller
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler
from telegram import InlineKeyboardButton,InlineKeyboardMarkup

#MSG DEFINED
REGISTER_REPLY_WRONG = "Ya está registrado, no debe usar mas este comando"
REGISTER_REPLY_GOOD = "Se acaba de registrar {}"
USER_NOT_REGISTERED = "Introduzca /start para crear una cuenta antes de hacer nada"
COMPRAR_REPLY = "Elige que quieres comprar:"
METE_DINERO_ARG_ERROR = "Argumentos invalidos, el formato de los comandos es \mete_dinero dinero"
METE_DINERO_REPLY = "TIENES {}€"
DINERO_REPLY = "TIENES {}€"
AYUDA_REPLY = '''Hola, este es el bot de gestion de la nevera de la onda
Si no pertenece a la onda y ha encontrado el bot, por favor ignorelo
Si es la primera vez que ejecuta el bot, por favor introduzca /start para crear un usuario
Dispone de los siguientes comandos:
/comprar despliega un menu con las opciones a comprar
 /dinero muestra su saldo
/metedinero dinero  añade dinero a su saldo
                 
No tiene limite negativo en el saldo,pero sea consecuente con las deudas
                 '''

#Callback Functions
def start(bot,update):
    #bot.send_message(chat_id=update.message.chat_id, text="Arrancado")
    usuario = update.message.from_user
    if db_controller.is_registered(usuario['id']):
        bot.send_message(chat_id=update.message.chat_id,text=REGISTER_REPLY_WRONG)
        return
    db_controller.crear_usuario(usuario['id'])
    bot.send_message(chat_id=update.message.chat_id,text=REGISTER_REPLY_GOOD.format(usuario['username']))
        
    
def comprar(bot,update,user_data):
    usuario = update.message.from_user
    if not db_controller.is_registered(usuario['id']):
        bot.send_message(chat_id=update.message.chat_id,text=USER_NOT_REGISTERED)
        return
    keyboard = gen_productos_keyboard()
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(COMPRAR_REPLY, reply_markup=reply_markup)   

def mete_dinero(bot,update,args):
    usuario = update.message.from_user
    if not db_controller.is_registered(usuario['id']):
        bot.send_message(chat_id=update.message.chat_id,text=USER_NOT_REGISTERED)
        return
    print(str(args))
    if len(args) != 1:
        bot.send_message(chat_id=update.message.chat_id,text=METE_DINERO_ARG_ERROR)
        return
    usuario = update.message.from_user
    user_id = usuario['id']
    cantidad = float(args[0])
    dinero = db_controller.add_dinero(user_id,cantidad)
    bot.send_message(chat_id=update.message.chat_id,text=METE_DINERO_REPLY.format(dinero))

def dinero(bot,update):
    usuario = update.message.from_user
    if not db_controller.is_registered(usuario['id']):
        bot.send_message(chat_id=update.message.chat_id,text=USER_NOT_REGISTERED)
        return
    user_id = usuario['id']
    bot.send_message(chat_id=update.message.chat_id,text=DINERO_REPLY.format(db_controller.get_dinero(user_id)))

def ayuda(bot,update):
    bot.send_message(chat_id=update.message.chat_id,text=AYUDA_REPLY)

#Callback query

def button(bot,update,user_data):
    query = update.callback_query
    print(user_data)
    usuario = query.from_user
    print("MI ID QUERY ES: "+str(usuario['id']))
    money = db_controller.comprar(usuario['id'],query.data)
    bot.edit_message_text(chat_id=query.message.chat_id,message_id=query.message.message_id,text="Opcion: {} \n Le quedan {} euros".format(query.data,money))

#Aux

def gen_productos_keyboard():
    lista_productos = db_controller.request_products()
    keyboard = []
    for elm in lista_productos:
        print(elm)
        keyboard.append([InlineKeyboardButton(str(elm),callback_data=str(elm))])
    print(keyboard)
    return keyboard
