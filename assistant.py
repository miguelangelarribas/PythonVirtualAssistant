import warnings
import pyttsx3
import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import datetime
import calendar
import random
import wikipedia

#pip install pyttsx3 text to speed
#pip install gtts  google text to speech
#pip install playsound
#pip install wikipedia


engine = pyttsx3.init()
#del engine cojo las voces y del engine seteo voz female
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def talk(audio):
    #al engine le pasamos un texto y el lo lee
    engine.say(audio)
    engine.runAndWait()

def rec_audio():
    """Graba el audio desde el micro y mira a ver si lo ha reconocido y nos lo devuelve como texto"""
    recog = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recog.listen(source)

    data = " "

    try:
        data = recog.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Assistan could not understan the audio")
    except sr.RequestError as ex:
        print("Request Error from Google Speech Recognition" + ex)

    return data

#talk("This is a test")

def response(text):
    """recibe un texto que lo pasa a google text to speech, guarda ese audio en un archivo lo reproduce y lo borra"""
    print(text)
    tts = gTTS(text=text, lang="en")

    audio = "Audio.mp3"
    tts.save(audio)
    playsound.playsound(audio)

    os.remove(audio)


def call(text):
    """coge un texto y si ese texto esta en actin call retorna true"""
    action_call = "assistant"

    text = text.lower()

    if action_call in text:
        return True

    return False

def today_date():
    """devuelve el dia de la semana mes y y dia ordinal"""
    now = datetime.datetime.now()
    date_now = datetime.datetime.today()
    #te devuelve el dia de la semana, lunes, martes
    week_now = calendar.day_name[date_now.weekday()]
    month_now = now.month
    day_now = now.day

    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December "
    ]

    ordinals = [
        "1st",
        "2nd",
        "3rd",
        "4th",
        "5th",
        "6th",
        "7th",
        "8th",
        "9th",
        "10th",
        "11st",
        "12nd",
        "13rd",
        "14th",
        "15th",
        "16th",
        "17th",
        "18th",
        "19th",
        "20th",
        "21st",
        "22nd",
        "23rd",
        "24th",
        "25th",
        "26th",
        "27th",
        "28th",
        "29th",
        "30th",
        "31st"
    ]

    return f'today is {week_now}, {months[month_now - 1]} the {ordinals[day_now - 1]}'

def say_hello(text):
    greet = ["hi", "hey", "hola", "greetings", "wassup", "hello", "howdy", "what's good", "hey there"]
    response = ["hi", "hey", "hola", "greetings", "wassup", "hello", "howdy", "what's good", "hey there"]

    for word in text.split():
        if word.lower() in greet:
            return random.choice(response) + "."

    return ""

def wiki_person(text):
    list_wiki = text.split()
    for i in range(0, len(list_wiki)):
        if i + 3 <= len(list_wiki) - 1 and list_wiki[i].lower() == "who" and list_wiki[i + 1].lower() == "is":
            return list_wiki[i + 2] + " " + list_wiki[i + 3]

while True:
    try:
        text = rec_audio()
        speak = " "
        #llamamos a call con el comando que hemos dicho por voz y si lo reconoce, nos devuelve el saludo
        if call(text):
            speak = speak + say_hello(text)

            if "date" in text or "day" in text or "month" in text:
                get_today = today_date()
                speak = speak + " " + get_today
            elif "time" in text:
                now = datetime.datetime.now()
                meridiem = ""
                if now.hour >= 12:
                    meridiem = "p.m"
                    hour = now.hour - 12
                else:
                    meridiem = "a.m"
                    hour = now.hour

                if now.minute < 10:
                    minute = "0" + str(now.minute)
                else:
                    minute = str(now.minute)
                speak = speak + " " + "It is " + str(hour) + ":" + minute + " " + meridiem + " ."

            elif "wikipedia" in text or "Wikipedia" in text:
                if "who is" in text:
                    person = wiki_person(text)
                    wiki = wikipedia.summary(person, sentences=2)
                    speak = speak + " " + wiki

            response(speak)
    except:
        talk("I don`t know that")

