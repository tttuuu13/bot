from flask import Flask, request
import telebot
import random
import os


server = Flask(__name__)
bot = telebot.TeleBot('5091025644:AAHdtFbTSvVL5LJVQqsQqo8rv9I3dJ1Uavw')

start_phrases = ['пошла нахуй', 'хуйню высрал', 'сука', 'ебншк????', 'отсоси', 'э']
oxxxy_phrases = ["говно", "залупа", "пенис", "хер", "давалка", "хуй", "блядина",
                 "головка", "шлюха", "жопа", "член", "еблан", "петух...", "мудила",
                 "рукоблуд", "ссанина", "очко", "блядун", "вагина", "сука", "ебланище",
                 "влагалище", "пердун", "дрочила", "пидор", "пизда", "туз", "малафья",
                 "гомик", "мудила", "пилотка", "манда", "анус", "вагина", "путана",
                 "пидрила", "шалава", "хуила", "мошонка", "елда", "РАУНД!"]


@bot.message_handler(commands=['start'])
def answer(message):
    name = message.from_user.first_name
    if message.chat.id == 947771996:
        bot.send_message(message.chat.id, f"ого! это же топ шха {name}!")
    else:
        bot.send_message(message.chat.id, f"Приветствую, {name}!")

@bot.message_handler(content_type=["text"], func=lambda message: message.text.lower() in oxxxy_phrases)
def battle(message):
    try:
        bot.send_message(message.chat.id, oxxxy_phrases[oxxxy_phrases.index(message.text.lower()) + 1])
    except:
        bot.send_message(message.chat.id, "втф")








@server.route('/' + '5091025644:AAHdtFbTSvVL5LJVQqsQqo8rv9I3dJ1Uavw', methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://shxa-bot.herokuapp.com/' + '5091025644:AAHdtFbTSvVL5LJVQqsQqo8rv9I3dJ1Uavw')
    return "!", 200

if __name__ == '__main__':
    server.debug = True
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
