import speech_recognition as sr
import os
import webbrowser
import openai
import pyttsx3
import datetime
import platform
import requests
import json
from dotenv import load_dotenv

load_dotenv()
engine = pyttsx3.init()
engine.setProperty('rate', 175)  
engine.setProperty('voice', 'english_rp+f3')  

# Configuration
WAKE_WORD = "hey deskbot"
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

# Predefined commands
COMMANDS = {
    "time": {
        "phrases": ["what time is it", "tell me the time", "current time"],
        "action": lambda: say(datetime.datetime.now().strftime("%I:%M %p"))
    },
    "date": {
        "phrases": ["what's today's date", "current date", "what day is it"],
        "action": lambda: say(datetime.datetime.now().strftime("%B %d, %Y"))
    }
}

def say(text):
    """Speak the given text aloud"""
    print(f"{text}")
    engine.say(text)
    engine.runAndWait()

def take_command(timeout=5):
    """Listen to user voice input and convert to text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = r.listen(source, timeout=timeout)
            print("Processing...")
            query = r.recognize_google(audio, language="en-in").lower()
            print(f"You: {query}")
            return query
        except sr.WaitTimeoutError:
            return ""
        except Exception as e:
            print(f"Error: {e}")
            say("Sorry, I didn't catch that.")
            return ""

def chat(query):
    """Handle conversation using OpenAI"""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": query}],
        temperature=0.7
    )
    answer = response.choices[0].message.content
    say(answer)
    return answer

def open_app(command):
    """Open applications based on command"""
    system = platform.system()
    app_commands = {
        "notepad": {
            "Windows": "notepad",
            "Darwin": "open -a TextEdit",
            "Linux": "gedit"
        },
        "calculator": {
            "Windows": "calc",
            "Darwin": "open -a Calculator",
            "Linux": "gnome-calculator"
        }
    }
    
    for app, commands in app_commands.items():
        if app in command:
            os.system(commands.get(system, ""))
            say(f"Opening {app}")
            return True
    return False

def get_weather(city="New York"):
    """Get weather information (requires API key)"""
    try:
        api_key = os.getenv('WEATHER_API_KEY')
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}appid={api_key}&q={city}"
        response = requests.get(complete_url)
        data = response.json()
        
        if data["cod"] != "404":
            main = data["main"]
            temperature = round(main["temp"] - 273.15, 1)
            weather = data["weather"][0]["description"]
            say(f"Current weather in {city}: {temperature}°C, {weather}")
        else:
            say("City not found")
    except Exception as e:
        say("Sorry, I couldn't fetch the weather")

def handle_command(query):
    """Process user commands"""
    # Check predefined commands
    for cmd, data in COMMANDS.items():
        if any(phrase in query for phrase in data["phrases"]):
            data["action"]()
            return True
    
    # Special cases
    if "open" in query:
        websites = {
            "youtube": "https://youtube.com",
            "google": "https://google.com",
            "wikipedia": "https://wikipedia.org"
        }
        for site, url in websites.items():
            if site in query:
                webbrowser.open(url)
                say(f"Opening {site}")
                return True
        return open_app(query)
    
    elif "weather" in query:
        city = query.split("in ")[-1] if "in " in query else "New York"
        get_weather(city)
        return True
    
    elif any(word in query for word in ["exit", "quit", "goodbye"]):
        say("Goodbye! Have a great day.")
        exit()
    
    return False

def main():
    """Main program loop"""
    say(f"DeskBot activated. Say '{WAKE_WORD}' to start.")
    
    while True:
        try:
            # Wait for wake word
            query = take_command()
            if not query or WAKE_WORD not in query:
                continue
                
            say("How can I help you?")
            query = take_command(timeout=8)
            
            if not query:
                continue
                
            # Try to handle command, fallback to AI chat
            if not handle_command(query):
                chat(query)
                
        except KeyboardInterrupt:
            say("Goodbye!")
            break

if __name__ == '__main__':
    main()
