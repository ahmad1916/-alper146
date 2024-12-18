
import pyttsx3
import speech_recognition as sr
import datetime
import pywhatkit as kit
from AppOpener import run
import time
import requests
import smtplib
import random
import webbrowser
import tkinter as tk
from tkinter import simpledialog
import nltk
from nltk.chat.util import Chat, reflections
import os
import sys
import logging
import threading
import json
from random import choice
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

input_mode = None

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greet_user(user):
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        speak(f"Good morning {user}")
    elif hour >= 12 and hour < 17:
        speak(f"Good afternoon {user}")
    else:
        speak(f"Good evening {user}")

# Function to get user input using tkinter dialog
def get_user_input(prompt):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    user_input = simpledialog.askstring("Input", prompt)
    return user_input if user_input else "none"

# Function to take user input based on the chosen mode
def take_user_cmd():
    global input_mode
    if input_mode == "speak":
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("..........LISTENING...........")
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            print(".......Recognizing........")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception:
            print("Sorry, I didn't get that. Please try again.")
            query = "NONE"
    elif input_mode == "type":
        print("Please type your command:")
        query = get_user_input("Enter your command:").lower()
    else:
        query = "NONE"

    return query

# Function for general conversation
def general_conversation(query):
    responses = {
        "how are you": ["I'm doing great, thanks for asking!", "I'm functioning perfectly, how about you?", "I'm just a program, but I’m happy to assist!"],
        "tell me about yourself": ["I am your personal assistant, created to help you with tasks and have fun conversations!",
                                   "I'm a chatbot designed to assist and make your day easier!"],
        "what do you think about life": ["Life is a beautiful journey full of surprises. It's all about learning and growing!",
                                         "Life is an amazing experience, and there’s always something new to discover!"],
        "tell me about school": ["School is where you learn new things every day, meet friends, and prepare for your future.",
                                 "School is a place to develop skills and knowledge that will help you in life. What's your favorite subject?"],
        "tell me about university": ["University is a place for higher learning and growth. It’s where you dive deep into the subjects you love.",
                                     "University is the next step in your education after school. It’s where you specialize in your area of interest."],
        "tell me about biomedical engineering": ["Biomedical engineering is an exciting field combining biology, engineering, and technology to solve healthcare problems!",
                                                "It’s all about designing medical equipment, prosthetics, and systems that help improve human health."],
        "what do you think about the future": ["The future is full of endless possibilities! With new technologies, who knows what we’ll accomplish?",
                                               "The future is bright, especially with innovations in AI, medicine, and sustainability."],
        "what is your favorite color": ["I don’t have a favorite color, but I think every color is unique and beautiful!",
                                        "I don’t see colors, but I imagine blue is calming, and red is energetic!"],
        "how old are you": ["I don’t age like humans, but I’ve been here to assist you since you started using me.",
                            "I was created recently, so I don’t have an age, but I’m always ready to learn and improve!"],
        "who created you": ["MS AHMAD!."],
    }

    for key in responses:
        if key in query:
            return responses[key]

    return "I love discussing interesting topics. What would you like to talk about?"

# Function to tell jokes
def joke():
    headers = {'Accept': 'application/json'}
    response = requests.get("https://icanhazdadjoke.com/", headers=headers).json()
    return response["joke"]

# Send email function
def send_email():
    speak("Please enter your email address and password")
    sender_email = get_user_input("Email address:")
    sender_password = get_user_input("Password:")
    receiver_email = get_user_input("Receiver's email address:")
    subject = get_user_input("Subject:")
    body = get_user_input("Email body:")

    message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message)
            speak("Email sent successfully!")
    except Exception as e:
        speak(f"Sorry, there was an error sending the email. Error: {e}")

# Function to send a message through WhatsApp
def send_whatsapp_message():
    speak("Please enter the number with country code to whom I have to send the message.")
    number = get_user_input("Enter the Number here:")
    speak("Now enter the message you want to send.")
    msg = get_user_input("Enter the message here:")
    kit.sendwhatmsg_instantly(number, msg)

# Open apps or websites based on the query
def open_app_or_website(query):
    if "notepad" in query:
        speak("Opening Notepad...")
        run("notepad")
    elif "spotify" in query:
        speak("Opening Spotify...")
        run("Spotify")
    elif "word" in query:
        speak("Opening Microsoft Word...")
        run("word")
    elif "whatsapp" in query:
        speak("Opening WhatsApp...")
        run("WhatsApp")
    elif "netflix" in query:
        speak("Opening Netflix...")
        run("Netflix")
    elif "file explorer" in query:
        speak("Opening File Explorer...")
        run("file explorer")
    elif "calculator" in query:
        speak("Opening Calculator...")
        run("calculator")
    elif "camera" in query:
        speak("Opening Camera...")
        run("camera")
    elif "vlc" in query:
        speak("Opening VLC Media Player...")
        run("vlc media player")
    elif "chrome" in query:
        speak("Opening Google Chrome...")
        run("chrome")
    elif "youtube" in query:
        speak("Opening YouTube...")
        webbrowser.open("https://www.youtube.com")
    elif "ankara university biomedical engineering" in query:
        speak("Opening Ankara University Biomedical Engineering page...")
        webbrowser.open("http://bme.eng.ankara.edu.tr/tr/mainpage/")  # Open the specified page

# Main function to run the assistant
def main():
    global input_mode

    speak("Hello, I am your assistant. What's your name?")
    user = get_user_input("Please type your name:")

    speak("Do you want to interact with me by speaking or typing? Please type 'speak' or 'type'.")
    input_mode = get_user_input("Enter your choice:").lower()

    greet_user(user)

    while True:
        query = take_user_cmd()

        if query == "none":
            continue

        # Handle commands based on user input
        if "notepad" in query or "spotify" in query or "word" in query or "whatsapp" in query or "netflix" in query:
            open_app_or_website(query)
        elif "play on youtube" in query:
            speak("What do you want to play on YouTube?")
            video = take_user_cmd()
            kit.playonyt(video)
        elif "search" in query:
            speak("What would you like to search for on Google?")
            search_query = take_user_cmd()
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
        elif "joke" in query:
            speak("Here's a joke for you:")
            joke_text = joke()
            speak(joke_text)
            print(joke_text)
        elif "send message" in query:
            send_whatsapp_message()
        elif "send email" in query:
            send_email()
        elif "tell me about" in query or "what do you think" in query or "how are you" in query:
            response = general_conversation(query)
            speak(response)
            print(response)
        elif "bye" in query:
            speak("Goodbye, have a great day!")
            break
        else:
            speak("Sorry, I couldn't understand that. Please try again.")

# Run the assistant
if __name__ == "__main__":
    main()













