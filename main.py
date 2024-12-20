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

#Функция для поиска песни по названию
@bot.message_handler(commands=['search'])
def search_song(message):
    song_name = message.text.replace('/search', '').strip()
    if not song_name:
        bot.reply_to(message, "Пожалуйста, укажите название песни после команды.")
        return

    url = f"https://api.genius.com/search?q={song_name}&access_token={GENIUS_API_KEY}"
    response = requests.get(url).json()

    if response['response']['hits']:
        song = response['response']['hits'][0]['result']
        song_url = song['url']
        song_title = song['title']
        song_artist = song['primary_artist']['name']
        bot.reply_to(message, f"Нашел песню: {song_title} от {song_artist}\nСсылка: {song_url}")
    else:
        bot.reply_to(message, "Песню не найдено. Попробуйте другой запрос.")

#Функция для получения текста песни по ID
@bot.message_handler(commands=['lyrics'])
def get_lyrics(message):
    song_id = message.text.replace('/lyrics', '').strip()
    if not song_id:
        bot.reply_to(message, "Пожалуйста, укажите ID песни после команды.")
        return

    url = f"https://api.genius.com/songs/{song_id}?access_token={GENIUS_API_KEY}"
    response = requests.get(url).json()

    if 'response' in response and 'song' in response['response']:
        song = response['response']['song']
        lyrics_url = song['url']
        bot.reply_to(message, f"Текст песни доступен по ссылке: {lyrics_url}")
    else:
        bot.reply_to(message, "Песня с таким ID не найдена.")
