from flask import Flask, request
import telebot
import random
import os
from aws import upload_file, download_file
import io

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from aws import upload_file
from phrases import oxxxy_phrases


server = Flask(__name__)
bot = telebot.TeleBot('5091025644:AAHdtFbTSvVL5LJVQqsQqo8rv9I3dJ1Uavw')


user_dict = {}

class Formula:
    def __init__(self):
        self.name = None
        self.description = None
        self.picture = None
        self.last_message = None
        self.file_name = None

@bot.message_handler(commands=['start'])
def answer(message):
    name = message.from_user.first_name
    #конфигурация кнопок
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add("Добавить формулу")
    
    if message.chat.id == 947771996:
        bot.send_message(message.chat.id, f"ого! это же топ шха {name}!", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, f"Приветствую, {name}!", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text.lower() in oxxxy_phrases)
def oxxxy(message):
    bot.send_message(message.chat.id, oxxxy_phrases[oxxxy_phrases.index(message.text.lower()) + 1])

@bot.message_handler(func=lambda message: message.text == "Добавить формулу")
def ask_for_name(message):
    user_dict[message.chat.id] = Formula()
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Не буду", callback_data="exit"))
    m = bot.send_message(message.chat.id, "Скинь название формулы, правила или закона", reply_markup=markup)
    user_dict[message.chat.id].last_message = m
    bot.register_next_step_handler(message, ask_description)

def ask_description(message):
    user_dict[message.chat.id].name = message.text
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Лучше отправлю картинку", callback_data="skip1"))
    markup.add(InlineKeyboardButton("Хочу выйти", callback_data="exit"))
    m = bot.send_message(message.chat.id, "Укажи описание, если оно нужно", reply_markup=markup)
    bot.register_next_step_handler(message, ask_picture)
    bot.edit_message_reply_markup(message.chat.id, user_dict[message.chat.id].last_message.message_id)
    user_dict[message.chat.id].last_message = m

def ask_picture(message):
    if user_dict[message.chat.id].description != "skip":
        user_dict[message.chat.id].description = message.text 
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Хватит и текста, го дальше", callback_data="skip2"))
    markup.add(InlineKeyboardButton("Хочу выйти", callback_data="exit"))
    m = bot.send_message(message.chat.id, "Можешь отправить картинку, а можешь и не отправлять", reply_markup=markup)
    bot.register_next_step_handler(message, upload_data)
    bot.edit_message_reply_markup(message.chat.id, user_dict[message.chat.id].last_message.message_id)
    user_dict[message.chat.id].last_message = m

def upload_data(message):
    try:
        bot.edit_message_reply_markup(message.chat.id, user_dict[message.chat.id].last_message.message_id)
    except:
        pass
    formula = user_dict[message.chat.id]
    if formula.picture == "skip" and formula.description == "skip":
        bot.send_message(message.chat.id, "Ты норм? Ничего кроме названия нет")
        return
    elif formula.picture == "skip":
        bot.send_message(message.chat.id, "Готово! Проверь пж")
        markup = InlineKeyboardMarkup(row_width=2)
        markup.row(InlineKeyboardButton("норм", callback_data="upload"),
                   InlineKeyboardButton("какиш", callback_data="exit"))
        m = bot.send_message(message.chat.id, f"*{formula.name}*\n\n{formula.description}",
                         parse_mode='Markdown', reply_markup=markup)
        user_dict[message.chat.id].last_message = m
        return
    elif message.photo == None:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("Хватит и текста, го дальше", callback_data="skip2"))
        markup.add(InlineKeyboardButton("Хочу выйти", callback_data="exit"))
        m = bot.send_message(message.chat.id, "Ну скинь фотку, че ты", reply_markup=markup)
        bot.register_next_step_handler(message, upload_data)
        user_dict[message.chat.id].last_message = m
        return
    elif formula.description == "skip":
        picture = bot.download_file(bot.get_file(message.photo[-1].file_id).file_path)
        user_dict[message.chat.id].picture = picture
        user_dict[message.chat.id].file_name = message.photo[-1].file_id
        markup = InlineKeyboardMarkup(row_width=2)
        markup.row(InlineKeyboardButton("норм", callback_data="upload"),
                   InlineKeyboardButton("какиш", callback_data="exit"))
        bot.send_message(message.chat.id, "Готово! Проверь пж")
        m = bot.send_photo(message.chat.id, picture, f"*{formula.name}*", parse_mode='Markdown',
                           reply_markup=markup)
        user_dict[message.chat.id].last_message = m
        return
    picture = bot.download_file(bot.get_file(message.photo[-1].file_id).file_path)
    user_dict[message.chat.id].picture = picture
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(InlineKeyboardButton("норм", callback_data="upload"),
               InlineKeyboardButton("какиш", callback_data="exit"))
    bot.send_message(message.chat.id, "Готово! Проверь пж")
    m = bot.send_photo(message.chat.id, picture, f"*{formula.name}*\n\n{formula.description}", parse_mode='Markdown',
                       reply_markup=markup)
    user_dict[message.chat.id].last_message = m

@bot.callback_query_handler(lambda query: query.data == "exit")
def exit(query):
    bot.clear_step_handler_by_chat_id(query.message.chat.id)
    bot.send_message(query.message.chat.id, "ну ок.")
    try:
        bot.edit_message_reply_markup(query.message.chat.id, user_dict[query.message.chat.id].last_message.message_id)
    except:
        pass

@bot.callback_query_handler(lambda query: query.data == "skip1")
def skip(query):
    try:
        user_dict[query.message.chat.id].description = "skip"
        bot.clear_step_handler_by_chat_id(query.message.chat.id)
        ask_picture(query.message)
    except:
        bot.send_message(query.message.chat.id, "упс, что-то не сработало")

@bot.callback_query_handler(lambda query: query.data == "skip2")
def skip(query):
    try:
        user_dict[query.message.chat.id].picture = "skip"
        bot.clear_step_handler_by_chat_id(query.message.chat.id)
        upload_data(query.message)
    except:
        bot.send_message(query.message.chat.id, "упс, что-то не сработало")


@bot.callback_query_handler(lambda query: query.data == "upload")
def upload_to_db(query):
    formula = user_dict[query.message.chat.id]
    try:
        bot.edit_message_reply_markup(query.message.chat.id, user_dict[query.message.chat.id].last_message.message_id)
    except:
        pass
    if formula.picture != "skip":
        r = upload_file(io.BytesIO(formula.picture), f"{formula.file_name}.png")
        if r:
            bot.send_message(query.message.chat.id, "Готово!")
        else:
            bot.send_message(query.message.chat.id, f"втфэшка, перешли это сообщение @tttuuu:\n{r}")



bot.delete_webhook()
bot.polling()