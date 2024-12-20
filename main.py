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

#Функция для получения информации об исполнителе
@bot.message_handler(commands=['artist'])
def get_artist_info(message):
    artist_name = message.text.replace('/artist', '').strip()
    if not artist_name:
        bot.reply_to(message, "Пожалуйста, укажите имя исполнителя после команды.")
        return

    url = f"https://api.genius.com/search?q={artist_name}&access_token={GENIUS_API_KEY}"
    response = requests.get(url).json()

    if response['response']['hits']:
        artist = response['response']['hits'][0]['result']['primary_artist']
        artist_name = artist['name']
        artist_url = artist['url']
        bot.reply_to(message, f"Информация об исполнителе:\nИмя: {artist_name}\nСсылка: {artist_url}")
    else:
        bot.reply_to(message, "Информация об исполнителе не найдена.")

#Функция для получения популярных песен
@bot.message_handler(commands=['top_songs'])
def top_songs(message):
    # Список популярных артистов
    popular_artists = ["Taylor Swift", "Drake", "Adele", "The Weeknd", "Ed Sheeran", "Lil Peep"]

    response_text = "Популярные песни:\n"
    for artist in popular_artists:
        url = f"https://api.genius.com/search?q={artist}&access_token={GENIUS_API_KEY}"
        response = requests.get(url).json()

        if response['response']['hits']:
            # Берем первую песню каждого исполнителя
            song = response['response']['hits'][0]['result']
            song_title = song['title']
            song_artist = song['primary_artist']['name']
            response_text += f"- {song_title} от {song_artist}\n"

    bot.reply_to(message, response_text)

#Рандомная песня от исполнителя
@bot.message_handler(commands=['random_song'])
def random_song(message):
    artist_name = message.text.replace('/random_song', '').strip()
    if not artist_name:
        bot.reply_to(message, "Пожалуйста, укажите имя исполнителя после команды.")
        return

    url = f"https://api.genius.com/search?q={artist_name}&access_token={GENIUS_API_KEY}"
    response = requests.get(url).json()

    if response['response']['hits']:
        songs = response['response']['hits']
        random_song = random.choice(songs)['result']
        song_title = random_song['title']
        song_artist = random_song['primary_artist']['name']
        song_url = random_song['url']
        bot.reply_to(message, f"Случайная песня от {song_artist}:\n{song_title}\nСсылка: {song_url}")
    else:
        bot.reply_to(message, "Песни этого исполнителя не найдены.")

#Поиск песен по тексту
@bot.message_handler(commands=['find_by_lyrics'])
def find_by_lyrics(message):
    lyrics_snippet = message.text.replace('/find_by_lyrics', '').strip()
    if not lyrics_snippet:
        bot.reply_to(message, "Пожалуйста, укажите текст песни после команды.")
        return

    url = f"https://api.genius.com/search?q={lyrics_snippet}&access_token={GENIUS_API_KEY}"
    response = requests.get(url).json()

    if response['response']['hits']:
        song = response['response']['hits'][0]['result']
        song_title = song['title']
        song_artist = song['primary_artist']['name']
        song_url = song['url']
        bot.reply_to(message, f"Песня с текстом '{lyrics_snippet}':\n{song_title} от {song_artist}\nСсылка: {song_url}")
    else:
        bot.reply_to(message, "Не удалось найти песню с таким текстом.")

#Сравнение популярности исполнителей
@bot.message_handler(commands=['compare_artists'])
def compare_artists(message):
    artists = message.text.replace('/compare_artists', '').strip().split(',')
    if len(artists) != 2:
        bot.reply_to(message, "Пожалуйста, укажите двух исполнителей через запятую.")
        return

    artist1, artist2 = [artist.strip() for artist in artists]

    def count_songs(artist_name):
        url = f"https://api.genius.com/search?q={artist_name}&access_token={GENIUS_API_KEY}"
        response = requests.get(url).json()
        return len(response['response']['hits'])

    count1 = count_songs(artist1)
    count2 = count_songs(artist2)

    if count1 > count2:
        bot.reply_to(message, f"{artist1} популярнее, у них {count1} песен, найденных на Genius, против {count2} у {artist2}.")
    elif count2 > count1:
        bot.reply_to(message, f"{artist2} популярнее, у них {count2} песен, найденных на Genius, против {count1} у {artist1}.")
    else:
        bot.reply_to(message, f"{artist1} и {artist2} одинаково популярны, у каждого по {count1} песен, найденных на Genius.")

#Обработчик некорректных команд
@bot.message_handler(func=lambda message: True)
def unknown_command(message):
    bot.reply_to(message, "Неизвестная команда. Используйте /start, чтобы увидеть список доступных команд.")

#Запуск бота
bot.polling(none_stop=True)
