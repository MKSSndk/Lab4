import telebot
import requests
import random

API_TOKEN = ''
GENIUS_API_KEY = ''

bot = telebot.TeleBot(API_TOKEN)

#Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    start_text = (
        "Привет! Я бот для работы с сервисом Genius.\n\n"
        "Вот список доступных команд:\n"
        "/start - показать это сообщение\n"
        "/search <song_name> - поиск текста песни по названию\n"
        "/lyrics <song_id> - показать текст песни по ID\n"
        "/artist <artist_name> - информация об исполнителе\n"
        "/top_songs - список популярных песен\n"
        "/random_song <artist_name> - случайная песня от исполнителя\n"
        "/find_by_lyrics <lyrics_snippet> - поиск песни по тексту\n"
        "/compare_artists <artist1>, <artist2> - сравнить популярность двух исполнителей\n"
    )
    bot.reply_to(message, start_text)
