import pyttsx3
import speech_recognition as sr
import datetime
import os
import webbrowser
import psutil
import random
import wikipedia
import re
import pyautogui
import ctypes
import subprocess
import shutil
import requests
import feedparser
import cv2
import time
import sys
from pyzbar.pyzbar import decode
from googletrans import Translator
import screen_brightness_control as sbc  

# ============== CONFIG ==============
ASSISTANT_NAME = "Luca"
USER_NAME = "Joel"
WAKE_WORD = f"hey {ASSISTANT_NAME.lower()}"
# ====================================

# Dictionary setup
try:
    from PyDictionary import PyDictionary
    dictionary = PyDictionary()
except:
    dictionary = None

# Translator
translator = Translator()

# -------------------- Jokes Setup --------------------
try:
    import pyjokes
    def get_joke():
        return pyjokes.get_joke()
except Exception:
    jokes_fallback = [
        "Why don't scientists trust atoms? Because they make up everything.",
        "I told my computer I needed a break, and it said no problem — it needed one too.",
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "Why did the programmer quit his job? Because he didn't get arrays."
    ]
    def get_joke():
        return random.choice(jokes_fallback)

# -------------------- AI Conversation --------------------
responses = {
    "hello": ["Hi there!", f"Hello, {USER_NAME}!", "Hey, how can I help?"],
    "how are you": ["I’m doing great!", "Feeling futuristic today!", "All systems running smoothly."],
    "your name": [f"I am {ASSISTANT_NAME}, your AI assistant."],
    "bye": ["Goodbye!", "See you later!", "Shutting down conversation."]
}
def ai_conversation(user_input):
    user_input = user_input.lower()
    for key in responses:
        if key in user_input:
            return random.choice(responses[key])
    return "Hmm, I don't understand that yet."

# -------------------- TTS Engine --------------------
engine = pyttsx3.init()
def speak(text):
    print(f"{ASSISTANT_NAME}: {text}")
    engine.say(text)
    engine.runAndWait()

speak(f"Hello {USER_NAME}, I am {ASSISTANT_NAME}. Ready to assist you.")

# -------------------- Voice Recognition --------------------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio, language="en-in")
        print(f"You said: {command}")
        return command.lower()
    except:
        return ""

# -------------------- Wake Word --------------------
def wait_for_wake_word():
    while True:
        command = listen()
        if WAKE_WORD in command:
            speak(f"Yes {USER_NAME}?")
            return

# -------------------- Command Input --------------------
def get_command():
    choice = input("\nPress [V] for Voice or [T] for Text (Q to Quit): ").lower()
    if choice == "q":
        return "exit"
    elif choice == "v":
        wait_for_wake_word()
        return listen()
    elif choice == "t":
        text = input("Type your command: ").lower()
        if WAKE_WORD in text:
            speak(f"Yes {USER_NAME}?")
            return input("Now type your command: ").lower()
        return text
    else:
        print("Invalid option.")
        return ""

# -------------------- Open Apps/Websites --------------------
def open_app_or_website(app_name):
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "paint": "mspaint.exe",
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "chrome": "chrome.exe",
        "edge": "msedge.exe",
        "vlc": "vlc.exe",
        "cmd": "cmd.exe",
        "explorer": "explorer.exe",
        "whatsapp": "whatsapp.exe",
        "spotify": "spotify.exe",
        "zoom": "zoom.exe",
        "teams": "ms-teams.exe"
    }

    websites = {
        "youtube": "https://youtube.com",
        "instagram": "https://instagram.com",
        "gmail": "https://mail.google.com",
        "google": "https://google.com",
        "github": "https://github.com",
        "wikipedia": "https://wikipedia.org",
        "facebook": "https://facebook.com",
        "twitter": "https://twitter.com",
        "chatgpt": "https://chatgpt.com"
    }

    if app_name in apps:
        exe = apps[app_name]
        path = shutil.which(exe)
        if path:
            subprocess.Popen([exe])
            speak(f"Opening {app_name} application")
            return
        else:
            try:
                os.startfile(exe)
                return
            except:
                pass

    if app_name in websites:
        webbrowser.open(websites[app_name])
        speak(f"Opening {app_name} website")
        return

    if "." in app_name:
        url = app_name
        if not url.startswith("http"):
            url = "https://" + url
        webbrowser.open(url)
        speak(f"Opening {url}")
        return

    speak(f"Searching for {app_name} on Google")
    webbrowser.open(f"https://www.google.com/search?q={app_name}")

# -------------------- Features --------------------
def get_weather(location="Ambernath"):
    if not location:
        location = "Ambernath"
    try:
        url = f"https://wttr.in/{location}?format=3"
        response = requests.get(url)
        if response.status_code == 200:
            speak(response.text)
        else:
            speak("Sorry, I could not fetch weather right now.")
    except:
        speak("Error while fetching weather.")

def get_news():
    try:
        feed = feedparser.parse("http://feeds.bbci.co.uk/news/rss.xml")
        if not feed.entries:
            speak("No news found.")
            return
        speak("Here are the top news headlines:")
        for entry in feed.entries[:3]:
            speak(entry.title)
    except:
        speak("Sorry, I could not fetch the news.")

def scan_qr_code():
    cap = cv2.VideoCapture(0)
    speak("Opening camera for QR code scan. Show the QR code to the camera.")
    while True:
        ret, frame = cap.read()
        for qr in decode(frame):
            qr_data = qr.data.decode('utf-8')
            cap.release()
            cv2.destroyAllWindows()
            speak(f"QR Code detected: {qr_data}")
            print("QR Code Data:", qr_data)
            return
        cv2.imshow("QR Code Scanner - Press Q to Exit", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    speak("QR code scan cancelled.")

# ✅ Fixed get_meaning
def get_meaning(word):
    try:
        if dictionary:
            meaning = dictionary.meaning(word)
            if meaning:
                first_key = list(meaning.keys())[0]
                first_meaning = meaning[first_key][0]
                speak(f"The meaning of {word} is: {first_meaning}")
                return
        # fallback to wikipedia
        try:
            result = wikipedia.summary(word, sentences=1, auto_suggest=False, redirect=True)
            speak(result)
        except wikipedia.exceptions.DisambiguationError as e:
            speak(f"{word} may refer to multiple things, like {e.options[0]}")
        except wikipedia.exceptions.PageError:
            speak(f"Sorry, I could not find any page for {word}.")
    except Exception as e:
        speak(f"Sorry, I could not find the meaning of {word}.")
        print("Error in get_meaning:", e)

def translate_text(text, dest_lang="en"):
    try:
        translated = translator.translate(text, dest=dest_lang)
        speak(f"In {dest_lang}, that is: {translated.text}")
    except:
        speak("Sorry, translation failed.")

# 📸 Updated Take Photo
def take_photo(mode="photo"):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        save_path = os.path.join(os.path.expanduser("~"), "Pictures", f"{mode}_{datetime.datetime.now().strftime('%H%M%S')}.png")
        cv2.imwrite(save_path, frame)
        speak(f"{mode.capitalize()} taken and saved in your Pictures folder")
        # Open in Photos app
        try:
            if os.name == "nt":  # Windows
                os.startfile(save_path)
            elif sys.platform == "darwin":  # macOS
                subprocess.run(["open", save_path])
            else:  # Linux
                subprocess.run(["xdg-open", save_path])
        except Exception as e:
            print("Could not open photo:", e)
    cap.release()

# 🖼 Updated Take Screenshot
def take_screenshot():
    save_path = os.path.join(os.path.expanduser("~"), "Pictures", f"screenshot_{datetime.datetime.now().strftime('%H%M%S')}.png")
    screenshot = pyautogui.screenshot()
    screenshot.save(save_path)
    speak(f"Screenshot taken and saved in your Pictures folder")
    # Open in Photos app
    try:
        if os.name == "nt":  # Windows
            os.startfile(save_path)
        elif sys.platform == "darwin":  # macOS
            subprocess.run(["open", save_path])
        else:  # Linux
            subprocess.run(["xdg-open", save_path])
    except Exception as e:
        print("Could not open screenshot:", e)

def send_whatsapp_message(contact_name, message):
    try:
        whatsapp_id = "5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App"
        subprocess.Popen(["explorer.exe", f"shell:AppsFolder\\{whatsapp_id}"])
        pyautogui.hotkey("ctrl", "f")
        time.sleep(1)
        pyautogui.typewrite(contact_name)
        time.sleep(2)
        pyautogui.press("enter")
        pyautogui.typewrite(message)
        time.sleep(1)
        pyautogui.press("enter")
        speak(f"Message sent to {contact_name} on WhatsApp.")
    except Exception as e:
        speak("Sorry, I could not send the WhatsApp message.")
        print("Error:", e)

# -------------------- System Controls --------------------
def shutdown_pc():
    speak("Shutting down the computer...")
    os.system("shutdown /s /t 5")

def restart_pc():
    speak("Restarting the computer...")
    os.system("shutdown /r /t 5")

def lock_pc():
    speak("Locking the computer...")
    ctypes.windll.user32.LockWorkStation()

def volume_up():
    pyautogui.press("volumeup")
    speak("Volume increased.")

def volume_down():
    pyautogui.press("volumedown")
    speak("Volume decreased.")

def mute_volume():
    pyautogui.press("volumemute")
    speak("Volume toggled mute.")

def set_brightness(value):
    try:
        sbc.set_brightness(value)
        speak(f"Brightness set to {value} percent.")
    except Exception as e:
        speak("Could not set brightness.")
        print("Error:", e)

def get_brightness():
    try:
        current = sbc.get_brightness()
        if isinstance(current, list):
            current = current[0]
        speak(f"Current brightness is {current} percent.")
    except:
        speak("Could not get brightness.")

def system_info():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    speak(f"CPU usage is at {cpu} percent and RAM usage is at {ram} percent.")

# -------------------- Command Processing --------------------
def process_command(command):
    command = command.lower()

    if "time" in command:
        now = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {now}")

    elif "weather" in command:
        location = command.replace("weather", "").strip()
        get_weather(location)

    elif "news" in command:
        get_news()

    elif "scan qr" in command or "qr code" in command:
        scan_qr_code()

    elif "selfie" in command:
        take_photo("selfie")

    elif "photo" in command:
        take_photo("photo")

    elif "screenshot" in command:
        take_screenshot()

    elif "send whatsapp" in command:
        try:
            parts = command.replace("send whatsapp to", "").strip().split("saying")
            contact_name = parts[0].strip()
            message = parts[1].strip()
            send_whatsapp_message(contact_name, message)
        except:
            speak("Say like: send whatsapp to John saying Hello")

    elif "meaning of" in command or "what does" in command:
        word = command.replace("meaning of", "").replace("what does", "").replace("mean", "").strip()
        get_meaning(word)

    elif "translate" in command:
        match = re.search(r"translate (.+) to (\w+)", command)
        if match:
            text = match.group(1)
            lang = match.group(2)
            translate_text(text, lang)
        else:
            speak("Please say like: Translate hello to Spanish")

    elif "joke" in command:
        speak(get_joke())

    elif "open " in command:
        app_name = command.replace("open ", "").strip()
        open_app_or_website(app_name)

    elif "system info" in command or "cpu" in command or "ram" in command:
        system_info()

    elif "shutdown" in command:
        shutdown_pc()

    elif "restart" in command:
        restart_pc()

    elif "lock" in command:
        lock_pc()

    elif "volume up" in command:
        volume_up()

    elif "volume down" in command:
        volume_down()

    elif "mute" in command:
        mute_volume()

    elif "set brightness" in command:
        match = re.search(r"set brightness to (\d+)", command)
        if match:
            val = int(match.group(1))
            set_brightness(val)
        else:
            speak("Please say like: Set brightness to 70")

    elif "brightness" in command:
        get_brightness()

    elif "exit" in command or "stop" in command or "quit" in command:
        speak(f"Goodbye {USER_NAME}, powering down.")
        exit()

    elif command.strip() != "":
        speak(ai_conversation(command))

# -------------------- Main Loop --------------------
while True:
    command = get_command()
    process_command(command)

