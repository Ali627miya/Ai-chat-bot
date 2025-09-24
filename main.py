import speech_recognition as sr
import webbrowser
import pyttsx3
import pyaudio
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
# pip3 install pocketsphinx 

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = os.getenv("NEWS_API_KEY")

def speak(text):
    engine.say(text)
    engine.runAndWait()

def speak_old(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

#Initialize Pygame mixer
    pygame.mixer.init()

#Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

#play the MP3 file
    pygame.mixer.music.play()

# Keep the program running until the music stops playing
    while pygame.mixer.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiprocess(command):
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        return "OpenAI API key not configured. Set OPENAI_API_KEY env var."
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": command}]
    )
    return response.choices[0].message.content

def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif  "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open chatgpt" in c.lower():
        webbrowser.open("http://chatgpt.com")
        
    elif c.lower().startswith("play"):
        try:
            song = c.replace("play", "").strip().title()
            link = musicLibrary.music[song]
            if link:
                webbrowser.open(link)
                speak(f"PLaying {song}")
            else:
                speak("Song not found in the music library")
        except Exception as e:
            speak("There was an error playing song")
            print (e)
        
    elif "news" in c.lower():
        if not newsapi:
            speak("News API key not configured. Set NEWS_API_KEY.")
            return
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('article', [])
            
            # Print the healdines
            for article in articles[:5]:
                speak(article['title'])
    else:
        # Let OPenAI handle the request
        output = aiprocess(c)
        speak(output)

            
if __name__ == "__main__":
    speak("Initializing jarvis.....")
    while True:
    # Listen for the wake word "JArvis"
    # Obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=2)
        
        
        print("recognizing...")

# recognize speech using Sphinx
        try:
            with sr.Microphone() as source:
                print("Say something!")
                audio = r.listen(source, timeout=2)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("ya")
                # LIsten for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    
                    processcommand(command)
                    
        
        except Exception as e:
            print("Sphinx error; {0}".format(e))
            

#52d466d4c732472bab7e8ef8eb85844c