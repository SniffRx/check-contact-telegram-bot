import telebot # подключение библиотеки для работы с телеграм ботом
import requests # подключение библиотеки для работы с запросами
from telebot import types # подключение модуля для работы с типами
import sqlite3 # подключение библиотеки для работы с базами данных Sqlite

conn = sqlite3.connect('PhoneNumbers.db', check_same_thread=False) # подключение к базе данных
cursor = conn.cursor()

def db_check_table_val(phone: str): # Функция проверки (Пользователь есть в базе данных ?)
    result = cursor.execute(
        'SELECT id FROM phone_numbers WHERE phone = ?', (phone,)).fetchone() #Запрос в базу данных (Принимает телефон пользователя)
    conn.commit()
    return result

def db_update_table_val(phone: str): # Функция обновления
    result = cursor.execute('UPDATE phone_numbers SET verification = 1  WHERE phone = ?', (phone,)).fetchone() # Запрос на обновления поля (verification)
    conn.commit()
    return result

TOKEN = '' # TOKEN бота
bot = telebot.TeleBot(TOKEN) # Подключение бота (Запуск)

@bot.message_handler(commands=["start"]) # Обработка команды "start"
def start_command_handler(msg): # Получение сообщения
    kb = types.ReplyKeyboardMarkup() # Создание клавиатуры
    contactbtn = types.KeyboardButton(
        'Отправить контакт', request_contact=True) # Создание кнопки
    kb.add(contactbtn) # Добавление кнопки в главиатуру
    bot.send_message(msg.from_user.id, "Привет, пожалуйста подтвердите номер.", reply_markup=kb) # Ответ бота на сообщение "start"

@bot.message_handler(content_types=['contact']) # Обработка команды (contact) PS. Пользователь отправляет телефонный номер с типом 'contact'
def contact(message): # Функция contact
    if message.contact is not None and message.from_user.id == message.contact.user_id: # Условие (Данный телефонный номер пользователя?) и (Данный телефонный номер не пустой?)
        us_phone = message.contact.phone_number # Создание переменной с телефонным номером
        numb = db_check_table_val(us_phone) # Отправка запроса в базу данных на проверку (Данный телефон есть в базе данных ?)
        if numb: # Проверка запроса
            if numb[0] == us_phone: # Условие проверки телефона
                db_update_table_val(us_phone) # Обновление поля verification
                bot.send_message(message.from_user.id, "Вы успешно прошли проверку") # Отправка сообщения
                # requests.get('https://domen.ru', params={'key': us_phone},)
        else:
            print("Номера: " + us_phone + " Нет в базе данных") # Отправка сообщения

bot.polling(none_stop=True, interval=0) # Предотвращает закрытие бота
