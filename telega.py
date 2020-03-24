import telebot
import requests
from telebot import types
import sqlite3
import datetime
import urllib
import config

connect = sqlite3.connect('database.db')

cursor = connect.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS visit(
    id integer PRIMARY KEY AUTOINCREMENT NOT NULL,
    user_id integer,
    date date,
    time text
    )
""")

connect.commit()
connect.close()

token = config.token

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['картинка'])
def kartinka(message):
    url =  "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
    data = requests.get(url).json()
    print(data)

@bot.message_handler(commands=['aaa'])
def stikers(message):
    sticker_id = "CAACAgIAAxkBAAI3j156KxU4GiJUcsqdzifoyMPEf__sAALCAgACNnYgDgABCVvK9_vDHhgE"
    bot.sent_sticker(message.chat.id, sticker_id)

@bot.message_handler(commands=['start'])
def say_hello(message):

    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    user_id = message.from_user.id

    last_visits = cursor.execute("""
        SELECT *
        FROM visit
        WHERE user_id = (?)
        ORDER BY id DESC
    """, [user_id]).fetchall()

    if len(last_visits)!=0:
        reply_text = f"Привет! В последний раз вы заходили {last_visits[0][2]}"
    else:
        reply_text = "Hello, new user"

    time = datetime.datetime.now()
    date = datetime.date.today()

    cursor.execute("""
        INSERT INTO visit (user_id, date)
        VALUES(?,?)
    """, [user_id, time])

    connect.commit()
    connect.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('/start')
    btn2 = types.KeyboardButton('/valute')

    markup.add(btn1, btn2)

    bot.send_message(message.chat.id, reply_text, reply_markup=markup)

@bot.message_handler(regexp='привет')
def reply_to_hello(message):
    text = message.text
    bot.send_message(message.chat.id, f"О привет, {message.from_user.first_name} я тебя знаю")


@bot.message_handler(regexp='привет')
def reply_to_hello(message):
    text = message.text
    bot.send_message(message.chat.id, f"О привет, {message.from_user.first_name} я тебя знаю")

@bot.message_handler(commands=['text'])
def reply_to_text(message):
    text = message.text
    bot.send_message(message.chat.id, f"Вы написали {text}, я пока не умею это делать")

bot.polling()