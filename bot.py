import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import random
import io
from flask import Flask, request
import dtb
from PIL import Image
import phrases
from math import ceil
from search import search


server = Flask(__name__)
bot = telebot.TeleBot('5091025644:AAHdtFbTSvVL5LJVQqsQqo8rv9I3dJ1Uavw')
admins = [599040955, 947771996, 1141189705]

user_dict = {}


class Formula:
    def __init__(self):
        self.name = None
        self.description = None
        self.picture = None
        self.last_message = None
        self.formulas_list_message = None


# ПРИКОЛЬЧИКИ
# оксимирон
@bot.message_handler(func=lambda message: message.text != None and message.text.lower() in phrases.oxxxy_phrases)
def oxxxy(message):
    bot.send_message(message.chat.id, phrases.oxxxy_phrases[phrases.oxxxy_phrases.index(message.text.lower()) + 1])

# будет отвечать на слово, содержащее "бот"
@bot.message_handler(func=lambda message: message.text != None and "бот" in message.text.lower())
def answer(message):
    bot.send_message(message.chat.id, random.choice(phrases.bot_answer).format(name=message.from_user.first_name))


# КОМАНДЫ БОТА
@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add("Добавить формулу")
    if message.chat.id in admins:
        bot.send_message(message.chat.id, f"Привет, {name}, тебе доступны команды админа", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, f"Приветствую, {name}!", reply_markup=keyboard)

# посмотреть все формулы
@bot.message_handler(commands=['show_all'])
def reset(message):
    if message.chat.id not in user_dict.keys():
        user_dict[message.chat.id] = Formula()
    user_dict[message.chat.id].formulas_list_message = None
    show_all(message)
def show_all(message, page=1):
    markup = InlineKeyboardMarkup()
    if message.chat.id not in user_dict.keys():
        user_dict[message.chat.id] = Formula()
    names = dtb.get_names()
    for i in sorted(names)[10*(page-1):10*page]:
        name = i
        index = names.index(name)
        if len(i) > 25:
            i = f"{i[:25]}..."
        markup.add(InlineKeyboardButton(i, callback_data=f"open_{index}|{page}"))
    if ceil(len(dtb.get_names())/10) == 0:
        markup.add(InlineKeyboardButton("ничего нет", callback_data="ничего нет"))
    elif page == 1 and ceil(len(dtb.get_names())/10) == 1:
        pass
    elif page == 1:
        markup.add(InlineKeyboardButton("▶", callback_data=f"page_{page+1}"))
    elif page == ceil(len(dtb.get_names())/10):
        markup.add(InlineKeyboardButton("◀", callback_data=f"page_{page-1}"))
    else:
        markup.add(InlineKeyboardButton("◀", callback_data=f"page_{page-1}"),
                   InlineKeyboardButton("▶", callback_data=f"page_{page+1}"))
    if user_dict[message.chat.id].formulas_list_message != None:
        bot.edit_message_reply_markup(message.chat.id, user_dict[message.chat.id].formulas_list_message.message_id,
                                      reply_markup=markup)
    else:
        m = bot.send_message(message.chat.id, "Вот список всех формул в алфавитном порядке:", reply_markup=markup)
        user_dict[message.chat.id].formulas_list_message = m

@bot.callback_query_handler(func=lambda query: query.data[:5] == "page_")
def change_page(query):
    show_all(query.message, int(query.data[5:]))

@bot.callback_query_handler(func=lambda query: query.data[:5] == "open_")
def open(query):
    page = int(list(query.data.split("|"))[1])
    index = int(list(query.data.split("|"))[0][5:])
    r = dtb.get_by_index(index)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Удалить", callback_data=f"delete_{index}|{page}"),
               InlineKeyboardButton("Назад", callback_data=f"go_back_{page}"))
    bot.delete_message(query.message.chat.id, user_dict[query.message.chat.id].formulas_list_message.message_id)
    if r[1] != None and r[2] != None:
        m = bot.send_photo(query.message.chat.id, Image.open(io.BytesIO(r[2])), f'{r[0]}\n{r[1]}',
                       reply_markup=markup)
    elif r[1] != None:
        m = bot.send_message(query.message.chat.id, f'{r[0]}\n{r[1]}',
                         reply_markup=markup)
    else:
        m = bot.send_photo(query.message.chat.id, Image.open(io.BytesIO(r[2])), f'{r[0]}',
                       reply_markup=markup)
    user_dict[query.message.chat.id].formulas_list_message = m

@bot.callback_query_handler(func=lambda query: query.data[:8] == "go_back_")
def go_back(query):
    bot.delete_message(query.message.chat.id, user_dict[query.message.chat.id].formulas_list_message.message_id)
    user_dict[query.message.chat.id].formulas_list_message = None
    show_all(query.message, int(query.data[8:]))

@bot.callback_query_handler(func=lambda query: query.data[:7] == "delete_")
def delete(query):
    index = int(list(query.data.split("|"))[0][7:])
    page = list(query.data.split("|"))[1]
    dtb.delete_row(dtb.get_names()[index])
    query.data = f"go_back_{page}"
    go_back(query)

@bot.callback_query_handler(func=lambda query: query.data[:5] == "show_")
def show(query):
    index = int(query.data[5:])
    r = dtb.get_by_index(index)
    if r[1] != None and r[2] != None:
        bot.send_photo(query.message.chat.id, Image.open(io.BytesIO(r[2])), f'{r[0]}\n{r[1]}')
    elif r[1] != None:
        bot.send_message(query.message.chat.id, f'{r[0]}\n{r[1]}')
    else:
        bot.send_photo(query.message.chat.id, Image.open(io.BytesIO(r[2])), f'{r[0]}')


# ДОБАВЛЕНИЕ ФОРМУЛЫ
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
                   InlineKeyboardButton("не очень", callback_data="exit"))
        m = bot.send_message(message.chat.id, f"{formula.name}\n\n{formula.description}", reply_markup=markup)
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
                   InlineKeyboardButton("не очень", callback_data="exit"))
        bot.send_message(message.chat.id, "Готово! Проверь пж")
        m = bot.send_photo(message.chat.id, picture, f"{formula.name}",
                           reply_markup=markup)
        user_dict[message.chat.id].last_message = m
        return
    picture = bot.download_file(bot.get_file(message.photo[-1].file_id).file_path)
    user_dict[message.chat.id].picture = picture
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(InlineKeyboardButton("норм", callback_data="upload"),
               InlineKeyboardButton("не очень", callback_data="exit"))
    bot.send_message(message.chat.id, "Готово! Проверь пж")
    m = bot.send_photo(message.chat.id, picture, f"{formula.name}\n\n{formula.description}",
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
    counter = 0
    names = dtb.get_names()
    if formula.name in names:
        counter = 1
        while f"{formula.name} ({counter})" in names:
            counter += 1
    if counter != 0:
        formula.name = f"{formula.name} ({counter})"
    if formula.description != "skip" and formula.picture != "skip":
        r = dtb.add(formula.name, formula.description, formula.picture)
        if r:
            bot.send_message(query.message.chat.id, "Отлично, спасибо, что учишь меня новым вещам")
        else:
            bot.send_message(query.message.chat.id, f"втфэшка, перешли это сообщение @tttuuu:\n{r}")
    elif formula.description == "skip":
        r = dtb.add(formula.name, None, formula.picture)
        if r:
            bot.send_message(query.message.chat.id, "Отлично, спасибо, что учишь меня новым вещам")
        else:
            bot.send_message(query.message.chat.id, f"втфэшка, перешли это сообщение @tttuuu:\n{r}")
    else:
        r = dtb.add(formula.name, formula.description, None)
        if r:
            bot.send_message(query.message.chat.id, "Отлично, спасибо, что учишь меня новым вещам")
        else:
            bot.send_message(query.message.chat.id, f"втфэшка, перешли это сообщение @tttuuu:\n{r}")


# ПОИСК
@bot.message_handler(content_types=['text'])
def send(message):
    names = dtb.get_names()
    counter = 0
    same = []
    for name in names:
        if message.text.lower() in name.lower():
            counter += 1
            same.append(name)
    if counter > 1:
        if len(message.text) < 3:
            bot.send_message(message.chat.id, "уточни пожалуйста🥺")
            return
        markup = InlineKeyboardMarkup()
        for b in same:
            index = names.index(b)
            markup.add(InlineKeyboardButton(b, callback_data=f"show_{index}"))
        bot.send_message(message.chat.id, "уточни пожалуйста:", reply_markup=markup)
        return
    
    results = search(message.text)
    print(results)
    if results == [] or results[0][1] < 30:
        bot.send_message(message.chat.id, "Похоже ничего не найдено")
        return
    other = InlineKeyboardMarkup()
    for i in results[1:]:
        if i[1] > 30:
            index = names.index(i[0])
            other.add(InlineKeyboardButton(i[0], callback_data=f"show_{index}"))
        else:
            break
    index = names.index(results[0][0])
    r = dtb.get_by_index(index)
    if r[1] != None and r[2] != None:
        bot.send_photo(message.chat.id, Image.open(io.BytesIO(r[2])), f'{r[0]}\n{r[1]}')
        if results[1][1] > 30:
            bot.send_message(message.chat.id, "вот еще пара вариантов:", reply_markup=other)
    elif r[1] != None:
        bot.send_message(message.chat.id, f'{r[0]}\n{r[1]}')
        if results[1][1] > 30:
            bot.send_message(message.chat.id, "вот еще пара вариантов:", reply_markup=other)
    else:
        bot.send_photo(message.chat.id, Image.open(io.BytesIO(r[2])), f'{r[0]}')
        if results[1][1] > 30:
            bot.send_message(message.chat.id, "вот еще пара вариантов:", reply_markup=other)


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
