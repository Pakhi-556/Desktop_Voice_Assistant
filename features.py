import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import smtplib
import requests
import os
from sk import *
import re
import random
from requests.exceptions import RequestException
from hugchat import hugchat
import wikipedia
from gmail import *
import sqlite3



# Initialize the text-to-speech engine
def speak(audio):
    engine=pyttsx3.init('sapi5')
    voices=engine.getProperty('voices')

    engine.setProperty('voice',voices[1].id)##zira voice
    engine.setProperty('rate',160)##set rate the voice

    engine.say(audio)
    engine.runAndWait()
    

## for taking command
def get_user_response():
    
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio,language='en-in').lower()
        print(query)
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand that.")
        return 'None'
    except sr.RequestError as e:
        speak(f"Error: {e}")
        return 'None'
    return query    

# for ip address
def get_ip(_return=False):
    try:
        response = requests.get(f'http://ip-api.com/json/').json()
        if _return:
            return response
        else:
            return f'Your IP address is {response["query"]}'
    except KeyboardInterrupt:
        return None
    except requests.exceptions.RequestException:
        return None

#for weather api
def get_weather_info(city=''):
    # Make a request to OpenWeatherMap API (assuming you have an API key)
    try:
        if city:
            response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={wkey}&units=metric').json()
        else:
            response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={get_ip(True)["city"]}&appid={wkey}&units=metric').json()
        weather = f'It\'s {response["main"]["temp"]}° Celsius and {response["weather"][0]["main"]}\n' \
               f'But feels like {response["main"]["feels_like"]}° Celsius\n' \
               f'Wind is blowing at {round(response["wind"]["speed"] * 3.6, 2)}km/h\n' \
               f'Visibility is {int(response["visibility"] / 1000)}km'
        return weather
    except requests.exceptions.RequestException:
        return None
    except KeyboardInterrupt:
        return None
   
#3 for new api
def news():
  arr=[] 
# Define the API endpoint with the provided API key
  api_address="https://newsapi.org/v2/top-headlines?sources=google-news-in&apiKey="+newskey
# Send a GET request to the API endpoint and parse the JSON response
  json_data=requests.get(api_address).json()

  for i in range(3):
        arr.append('Headline '+str(i+1)+": "+json_data["articles"][i]['title']+'.')

  return arr


##for joke
def joke():
     # Example function to fetch a joke from a joke API
    api_address="https://official-joke-api.appspot.com/random_joke"
    json_data=requests.get(api_address).json()

    arr=["",""]
    arr[0]=json_data["setup"]
    arr[1]=json_data["punchline"]
    return arr  

## set reminder
def set_reminder():
    speak('What should I remember?')
    answer = get_user_response().lower()
    file_name = remember + '/remember.txt'
    file = open(file_name, 'w')
    file.write(answer)
    speak('Okay, I\'ll remember it')
    file.close()

##read remember
def read_remember():
    file_name = remember + '/remember.txt'
    file = open(file_name, 'r')
    speak(file.read())

def execute_command(command):
    pass 

def search_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)

def search_youtube(query):
    search_url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(search_url)

def search_google_maps(query):
    search_url = f"https://www.google.com/maps/search/{query}"
    webbrowser.open(search_url)

#play music
def play_music(song_name=None):
    music_dir = r"C:\Users\PAKHI\Music" 
    songs = os.listdir(music_dir)
    if song_name:
        if f"{song_name}.mp3" in songs:
            os.startfile(os.path.join(music_dir, f"{song_name}.mp3"))
        else:
            speak(f"{song_name} is not available locally. Would you like to play it on YouTube?")
            response = get_user_response()
            while response.lower() not in ['yes', 'no']:
                speak("Please say yes or no.")
                response = get_user_response()
            if response.lower() == 'yes':
                search_youtube(song_name)
                speak(f"Playing {song_name} on YouTube.")
            else:
                speak("Okay, no problem.")
    else:
        if songs:
            index = random.randint(0, len(songs) - 1)
            try:
                os.startfile(os.path.join(music_dir, songs[index]))
            except AttributeError:
                speak(f"Unable to play {songs[index]} locally. Would you like to search it on YouTube?")
                response = get_user_response()
                while response.lower() not in ['yes', 'no']:
                    speak("Please say yes or no.")
                    response = get_user_response()
                if response.lower() == 'yes':
                    search_youtube(songs[index])
                    speak(f"Playing {songs[index]} on YouTube.")
                else:
                    speak("Okay, no problem.")
        else:
            speak("No music files found in the directory.")

#function for movies 
def get_popular_movies():
    try:
        
        response = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={tmdbk}&region=IN&sort_by=popularity.desc&primary_release_year={datetime.date.today().year}").json()

        if 'results' in response and len(response['results']) > 0:
            # Print only the top 5 popular movies
            movie_titles = [movie['title'] for movie in response['results'][:3]]
            speak("Some of the latest popular movies are:")
            for title in movie_titles:
                speak(title)
    except requests.exceptions.RequestException:
        speak("Sorry, I couldn't fetch the popular movies at the moment.")

## integrate hugging api for chat bot
def chatBot(query):
    t=''
    print('Chatting...')
    user_input = query.lower()
    print(f"User : {user_input}")
    chatbot = hugchat.ChatBot(cookie_path="cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    t+='Zira : \t'
    t+=response
    return t

def ai(prompt):
    t=""
    text = f"AI response of promt : {prompt} \n ******** \n\n"
    chatbot = hugchat.ChatBot(cookie_path="cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(prompt)

    text+=response
    t+=response
    if not os.path.exists("Work_History"):
        os.makedirs("Work_History")

    with open(f"Work_history/{''.join(prompt.split('can you write')[1:30])}.txt", "w", encoding='utf-8') as f:
        f.write(text)
    return t  


def send_everyone(subject,body):

    # Fetch email addresses from the database
    conn = sqlite3.connect("sqlite.db")
    cursor = conn.cursor()
    cursor.execute("SELECT emp_email FROM employee")
    emails = cursor.fetchall()
    conn.close()

    # Send emails to each recipient
    for email in emails:
        recipient_email = email[0]
        send_email(recipient_email, subject, body)
        print(f"Email sent to: {recipient_email}")