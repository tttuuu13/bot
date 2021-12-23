from flask import Flask, request
import telebot
import random
import os


server = Flask(__name__)
bot = telebot.TeleBot('5091025644:AAHdtFbTSvVL5LJVQqsQqo8rv9I3dJ1Uavw')

start_phrases = ['пошла нахуй', 'хуйню высрал', 'сука', 'ебншк????', 'отсоси', 'э', 'ты солнце']


@bot.message_handler(commands=['start'])
def answer(message):
    x = random.choice([0, 1, 2, 3, 4, 5])
    if x > 0:
        bot.send_message(message.chat.id, random.choice(start_phrases))
    else:
        bot.send_sticker(message.chat.id, random.choice(['CAACAgIAAxkBAAEC4nZhO6XViAaTaT0ihQxTMtTtaelDSQACCAADwDZPE29sJgveGptpIAQ',
                                                         'CAACAgQAAxkBAAEDjBthxIECLvoOdIyZPPh1IHRgmlFTVgACvgoAArzKMVBTZLKRMN5o5yME',
                                                         'CAACAgQAAxkBAAEDjB1hxIE0RaUWsMSwrorvX0fQxEMK5QAC6AoAAt9QiFHGFAABQGOzE1cjBA']))








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
