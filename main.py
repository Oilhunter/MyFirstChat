from flask import Flask, render_template, url_for, request
from datetime import datetime
import json

app = Flask(__name__)


DB_FILE = "./data/db.json"  # Путь к файлу с сообщениям
db = open(DB_FILE, "rb")  # Открываем файл для чтения
data = json.load(db)  # Загрузить все данные в формате JSON  из файла
messages = data['messages']  # Из полученых данных берем поле messages


# Функция для сохранения всех сообщений (в списке message) в файл
def save_messages_to_file():
    db = open(DB_FILE, "w")  # Открываем файл для записи
    data = {  # Создаем структуру для записи в файл
         "messages": messages
    }
    json.dump(data, db)  # Запишем структуру в файл


def add_message(text, sender):  # Объявим функцию, которая добавит сообщение в список
    time_now = datetime.now().strftime('%H:%M')
    new_message = {
        'text': text,
        'sender': sender,
        'time': time_now,
    }
    messages.append(new_message)
    save_messages_to_file()


def print_message(message):  # Объявляем функцию, которая будет печатать одно сообщение
    print(f"[{message['sender']}]: {message['time']} {message['text']}")


# Главная страница
@app.route('/')
def index_page():
    return render_template('index.html')


#  Показать все сообщения в формате JSON
@app.route('/get_messages')
def get_messages():
    return {'messages': messages}


# Показать форму чата
@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/send_message')
def send_message():
    # Получить имя и текст от пользователя
    name = request.args['name']  # Получаем имя
    text = request.args['text']  # Получаем текс
    # Вызвать функцию add_message
    if len(name) < 2 or len(name) > 25:
        print("Длина имени пользователя недопустима")
    elif len(text) > 1000:
        print("Длина сообщения недопустима")
    else:
        add_message(text, name)
    return 'OK'


app.run()  # Запускает веб-приложение
