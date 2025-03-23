import tkinter as tk
from tkinter import scrolledtext, messagebox
import time
import webbrowser
import random
import speech_recognition as sr
import pyttsx3

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Global dark mode state 
is_dark_mode = False

# Simple rule-based chatbot responses
# Simple rule-based chatbot responses with science-related questions 
def chatbot_response(user_input):
    responses = {
        "hello": ["Hi there!", "Hello!", "Hey, how can I help?"],
        "how are you": ["I'm great, thanks for asking!", "Doing well, how about you?"],
        "who created you": ["I was created by a developer named Joel using Python and Tkinter!", "A skilled programmer brought me to life!"],
        "what is your name": ["I'm Jarvis, a chatbot.", "You can call me Jarvis!"],
        "what can you do": ["I can chat, answer science-related questions, and more!", "Providing scientific insights is my goal."],
        
        # Science-related questions
        "what is gravity": ["Gravity is a force that attracts two bodies toward each other. It keeps us on Earth!"],
        "how does photosynthesis work": ["Plants use sunlight, carbon dioxide, and water to produce oxygen and glucose through photosynthesis."],
        "what is an atom": ["An atom is the smallest unit of matter, made of protons, neutrons, and electrons."],
        "what is a black hole": ["A black hole is a region in space with an intense gravitational pull where nothing, not even light, can escape."],
        "how does a rocket work": ["A rocket works by expelling high-speed gases in the opposite direction, creating thrust that propels it forward."],
        "what is the speed of light": ["The speed of light in a vacuum is approximately 299,792 kilometers per second (186,282 miles per second)."],
        "what are the states of matter": ["The main states of matter are solid, liquid, gas, and plasma."],
        "how is electricity generated": ["Electricity is generated using energy sources like fossil fuels, nuclear power, wind, and solar panels."],
        "what is evolution": ["Evolution is the process by which organisms change over time through natural selection and genetic variation."],
        "what causes earthquakes": ["Earthquakes are caused by the movement of tectonic plates along fault lines."],
        "why is the sky blue": ["The sky appears blue because molecules in the atmosphere scatter shorter blue light waves more than other colors."],
        "what is DNA": ["DNA (deoxyribonucleic acid) is the molecule that carries genetic instructions for life."],
        "how does the human brain work": ["The brain processes information through neurons, which transmit electrical and chemical signals."],
        "why do we need sleep": ["Sleep helps our bodies and brains recover, consolidate memories, and maintain overall health."],
        "what is quantum mechanics": ["Quantum mechanics is a branch of physics that studies how particles behave at extremely small scales."],
        "what is the big bang theory": ["The Big Bang Theory explains how the universe began from a singularity and expanded over billions of years."],
        "how do vaccines work": ["Vaccines train the immune system to recognize and fight specific viruses or bacteria."],
        "what is dark matter": ["Dark matter is a mysterious, invisible substance that makes up most of the universe's mass."],
        "what is antimatter": ["Antimatter consists of particles with opposite charges to normal matter, like positrons instead of electrons."],
        "how do plants grow": ["Plants grow through cell division, photosynthesis, and absorbing nutrients from soil and water."],
        "what is nanotechnology": ["Nanotechnology involves manipulating materials at an atomic or molecular scale for advanced applications."],
        "how do we detect exoplanets": ["Scientists detect exoplanets using methods like the transit method and radial velocity measurements."],
        "what is artificial intelligence": ["Artificial Intelligence (AI) is the simulation of human intelligence in machines that can learn and adapt."],
        "can we live on mars": ["Living on Mars would require creating artificial habitats, oxygen generation, and protection from radiation."],
        "what is a gene": ["A gene is a segment of DNA that contains instructions for building proteins in living organisms."],
        "why do stars twinkle": ["Stars twinkle because their light is refracted by Earth's atmosphere as it passes through different air layers."],
        "what is nuclear fusion": ["Nuclear fusion is the process where atomic nuclei combine to release energy, like in the sun."],
        "what are black holes made of": ["Black holes are made of highly compressed matter with an immense gravitational pull."],
        "what is the function of the heart": ["The heart pumps blood, delivering oxygen and nutrients throughout the body."],
        "how do glasses work": ["Glasses use lenses to correct vision by bending light so it focuses properly on the retina."],
        "why is the ocean salty": ["Oceans are salty due to dissolved minerals and salts from rocks and river runoff over millions of years."],
        "how do birds fly": ["Birds fly by flapping their wings, using lift, thrust, drag, and gravity to stay airborne."],
        "what is sound": ["Sound is a vibration that travels through air, water, or solid objects as waves."],
    }
    return random.choice(responses.get(user_input.lower(), ["Sorry, I don't understand that."]))


# Function to update chat window
def send_message():
    user_text = entry_box.get().strip()
    if user_text:
        chat_window.insert(tk.END, f"🧑 You: {user_text}\n", "user")
        entry_box.delete(0, tk.END)

        # Typing delay simulation
        chat_window.insert(tk.END, "🤖 Jarvis is typing...\n", "typing")
        chat_window.update_idletasks()
        time.sleep(0.5)
        chat_window.delete("end-2l", "end")  # Remove typing indicator

        # Get bot response
        bot_text = chatbot_response(user_text)
        chat_window.insert(tk.END, f"\n🤖 Jarvis: {bot_text}\n", "Jarvis")

        # Speak the bot's response
        engine.say(bot_text)
        engine.runAndWait()

        # Store messages for export
        chat_history.append((user_text, bot_text))
        chat_window.yview(tk.END)

# Function for voice input
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        chat_window.insert(tk.END, "🎤 Listening...\n", "typing")
        chat_window.update_idletasks() 
        audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio)
            entry_box.delete(0, tk.END)
            entry_box.insert(0, user_input)
            send_message()
        except sr.UnknownValueError:
            chat_window.insert(tk.END, "🤖 Jarvis: Sorry, I did not understand that.\n", "Jarvis")
        except sr.RequestError:
            chat_window.insert(tk.END, "🤖 Jarvis: Could not request results from Google Speech Recognition service.\n", "Jarvis")

# Export chat history to HTML
def export_chat_to_html():
    html_content = """
    <html>
    <head>
        <title>Chat History</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }
            .chat-container { max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0px 0px 10px gray; }
            .user { color: blue; font-weight: bold; }
            .bot { color: green; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class='chat-container'>
    """
    for user_msg, bot_msg in chat_history:
        html_content += f"<p class='user'>🧑 You: {user_msg}</p>"
        html_content += f"<p class='bot'>🤖 Jarvis: {bot_msg}</p>"
    html_content += "</div></body></html>"

    with open("chat_history.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    webbrowser.open("chat_history.html")

# Clear chat history
def clear_chat():
    chat_window.delete(1.0, tk.END)
    chat_history.clear()

# Display help information 
def show_help():
    messagebox.showinfo("Help", "Available Commands:\n\n"
                                "1. hello\n"
                                "2. how are you\n"
                                "3. what is your name\n"
                                "4. who created you\n"
                                "5. what is gravity\n"
                                "6. how does photosynthesis work\n"
                                "7. what are the states of matter\n"
                                "8. what is artificial intelligence\n"
                                "9. how do birds fly\n"
                                "10. what is sound\n"
                                 )

# Dark mode toggle
def toggle_dark_mode():
    global is_dark_mode
    is_dark_mode = not is_dark_mode
    if is_dark_mode:
        root.configure(bg="#333333")
        chat_window.configure(bg="#1e1e1e", fg="#e0e0e0", insertbackground="#e0e0e0")
        entry_box.configure(bg="#1e1e1e", fg="#e0e0e0", insertbackground="#e0e0e0")
        dark_mode_button.config(text="🌞 Light Mode")

        # Update chat text colors
        chat_window.tag_config("user", foreground="#4ea8de", font=("Arial", 12, "bold"))
        chat_window.tag_config("Jarvis", foreground="#9cdcfe", font=("Arial", 12, "bold"))
        chat_window.tag_config("typing", foreground="#ffa500", font=("Arial", 10, "italic"))
    else:
        root.configure(bg="#f4f4f4")
        chat_window.configure(bg="white", fg="black", insertbackground="black")
        entry_box.configure(bg="white", fg="black", insertbackground="black")
        dark_mode_button.config(text="🌙 Dark Mode")

        # Revert to normal colors
        chat_window.tag_config("user", foreground="blue", font=("Arial", 12, "bold"))
        chat_window.tag_config("Jarvis", foreground="green", font=("Arial", 12, "bold"))
        chat_window.tag_config("typing", foreground="gray", font=("Arial", 10, "italic"))

# Initialize main Tkinter window
root = tk.Tk()
root.title("Jarvis Chatbot")
root.geometry("500x600")
root.configure(bg="#f4f4f4")

# Chat history list
chat_history = []

# Chat window
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='normal', font=("Arial", 12))
chat_window.tag_config("user", foreground="blue", font=("Arial", 12, "bold"))
chat_window.tag_config("Jarvis", foreground="green", font=("Arial", 12, "bold"))
chat_window.tag_config("typing", foreground="gray", font=("Arial", 10, "italic"))
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Entry box for user input
entry_box = tk.Entry(root, font=("Arial", 14))
entry_box.pack(padx=10, pady=10, fill=tk.X)
entry_box.bind("<Return>", lambda event: send_message())

# Button frame
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Send button
send_button = tk.Button(button_frame, text="Send", command=send_message)
send_button.grid(row=0, column=0, padx=5)

# Voice input button
voice_button = tk.Button(button_frame, text="🎤 Voice", command=voice_input)
voice_button.grid(row=0, column=1, padx=5)

# Export chat button
export_button = tk.Button(button_frame, text="Export", command=export_chat_to_html)
export_button.grid(row=0, column=2, padx=5)

# Clear chat button
clear_button = tk.Button(button_frame, text="Clear", command=clear_chat)
clear_button.grid(row=0, column=3, padx=5)

# Help button
help_button = tk.Button(button_frame, text="Help", command=show_help) 
help_button.grid(row=0, column=4, padx=5) 

# Dark mode toggle button
dark_mode_button = tk.Button(root, text="🌙 Dark Mode", command=toggle_dark_mode) 
dark_mode_button.pack(pady=5)

# Run the application
root.mainloop()
