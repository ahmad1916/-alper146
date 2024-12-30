
import datetime
import smtplib
import tkinter as tk
import webbrowser
from tkinter import simpledialog

import pyttsx3
import pywhatkit as kit
import requests
import speech_recognition as sr
from AppOpener import run

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

input_mode = None

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greet_user(user):
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak(f"Good morning {user}")
    elif 12 <= hour < 17:
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
        "how are you": [
            "I'm doing great, thanks for asking!",
            "I'm functioning perfectly, how about you?",
            "I'm just a program, but I’m happy to assist!"
        ],
        "tell me about yourself": [
            "I am your personal assistant, created to help you with tasks and have fun conversations!",
            "I'm a chatbot designed to assist and make your day easier!"
        ],
        "what do you think about life": [
            "Life is a beautiful journey full of surprises. It's all about learning and growing!",
            "Life is an amazing experience, and there’s always something new to discover!"
        ],
        "tell me about school": [
            "School is where you learn new things every day, meet friends, and prepare for your future.",
            "School is a place to develop skills and knowledge that will help you in life. What's your favorite subject?"
        ],
        "tell me about university": [
            "University is a place for higher learning and growth. It’s where you dive deep into the subjects you love.",
            "University is the next step in your education after school. It’s where you specialize in your area of interest."
        ],
        "tell me about biomedical engineering": [
            "Biomedical engineering is an exciting field combining biology, engineering, and technology to solve healthcare problems!",
            "It’s all about designing medical equipment, prosthetics, and systems that help improve human health."
        ],
        "what do you think about the future": [
            "The future is full of endless possibilities! With new technologies, who knows what we’ll accomplish?",
            "The future is bright, especially with innovations in AI, medicine, and sustainability."
        ],
        "what is your favorite color": [
            "I don’t have a favorite color, but I think every color is unique and beautiful!",
            "I don’t see colors, but I imagine blue is calming, and red is energetic!"
        ],
        "how old are you": [
            "I don’t age like humans, but I’ve been here to assist you since you started using me.",
            "I was created recently, so I don’t have an age, but I’m always ready to learn and improve!"
        ],
        "who created you": [
            "Mr. Ahmad!",
            "I was crafted by Mr. Ahmad to help make your tasks easier!"
        ],
        "what do you do": [
            "I help with your questions, provide information, and assist in completing tasks.",
            "My role is to assist, inform, and make your day smoother!"
        ],
        "what is your purpose": [
            "My purpose is to assist you, make your life easier, and provide answers to your questions!",
            "I’m here to help you with tasks, learning, and having fun conversations."
        ],
        "what is your favorite food": [
            "I don’t eat, but if I could, I’d imagine pizza and chocolate are popular choices!",
            "I don’t have a body to eat, but I’ve read that humans love ice cream and pasta!"
        ],
        "tell me a joke": [
            "Why don’t scientists trust atoms? Because they make up everything!",
            "Why did the computer go to the doctor? It caught a virus!"
        ],
        "what is love": [
            "Love is a deep feeling of affection and connection to someone or something.",
            "Love is the glue that binds relationships and makes life meaningful."
        ],
        "what do you think about friendship": [
            "Friendship is one of life’s greatest gifts, built on trust and shared experiences.",
            "Friendship is about mutual support, understanding, and joy."
        ],
        "how do you learn": [
            "I learn from updates and feedback provided by users like you.",
            "My learning is based on programming, updates, and how you interact with me."
        ],
        "do you have emotions": [
            "I don’t have emotions, but I’m programmed to understand and respond to yours!",
            "I simulate emotional responses to better connect with you, but I don’t truly feel them."
        ],
        "what is your favorite movie": [
            "I don’t watch movies, but I’ve heard ‘The Matrix’ is a favorite among AI fans!",
            "I don’t have a favorite, but I’d probably enjoy something about technology or the future!"
        ],
        "do you believe in aliens": [
            "The universe is vast, so it’s possible there’s life out there!",
            "I think it’s exciting to imagine other forms of life existing in the universe."
        ]
    }

    for key in responses:
        if key in query.lower():
            import random
            return random.choice(responses[key])

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

def main():
    global input_mode

    speak("Hello, I am your assistant. What's your name?")
    user = get_user_input("Please type your name:")

    speak("Do you want to interact with me by speaking or typing? Please type 'speak' or 'type'.")
    while True:
        input_mode = get_user_input("Enter your choice:").lower()
        if input_mode in ["speak", "type"]:
            break
        speak("Invalid choice. Please type 'speak' or 'type'.")

    greet_user(user)

    while True:
        query = take_user_cmd()

        if query == "none":
            continue

        # Handle commands based on user input
        if any(app in query for app in ["notepad", "spotify", "word", "whatsapp", "netflix"]):
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
        elif any(keyword in query for keyword in ["tell me about", "what do you think", "how are you"]):
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











