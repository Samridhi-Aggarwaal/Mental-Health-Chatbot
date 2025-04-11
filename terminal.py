import customtkinter as ctk
import tkinter.messagebox as messagebox
import nltk
from nltk.chat.util import Chat, reflections


nltk.download('punkt')


pairs = [
    [
        r"(.*)(your name|who are you)(.*)",
        ["My name is EmpathyBot. I’m your emotional support companion. ❤️"]
    ],
    [
        r"(hi|hey|hello)",
        ["Hello there! How are you feeling today? 😊"]
    ],
    [
        r"(.*)(help)(.*)",
        ["I'm here to help. Please tell me what's going on."]
    ],
    [
        r"(.*)(sad|depressed|unhappy|lonely)(.*)",
        ["I'm really sorry you're feeling that way. I'm here to listen, no judgment."]
    ],
    [
        r"(.*)(anxious|stressed|panic)(.*)",
        ["That sounds tough. Remember to breathe slowly. You're not alone."]
    ],
    [
        r"(.*)(happy|excited|joy)(.*)",
        ["That's wonderful to hear! Tell me more about it. 😄"]
    ],
    [
        r"(.*)(thank you|thanks)(.*)",
        ["You're always welcome! I'm glad to be here for you."]
    ],
    [
        r"(bye|exit|quit)",
        ["Goodbye! Take care of yourself. 🌸"]
    ],
    [
        r"(.*)",
        ["Hmm... can you tell me a bit more?", "I'm listening... ❤️"]
    ]
]

chatbot = Chat(pairs, reflections)

def chatbot_response(user_input):
    return chatbot.respond(user_input)



# Set theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")  # Other options: green, dark-blue, etc.

# Create app window
app = ctk.CTk()
app.title("Mental Health Chatbot - EmpathyBot")
app.geometry("600x520")
app.resizable(False, False)

# Title
title_label = ctk.CTkLabel(app, text="🧠 EmpathyBot - Your Mental Health Companion", font=("Helvetica", 20, "bold"))
title_label.pack(pady=20)

# Chat display box
chat_display = ctk.CTkTextbox(app, width=550, height=300, font=("Helvetica", 14), wrap="word")
chat_display.pack(pady=10)
chat_display.insert("end", "EmpathyBot: Hi there! I'm here to support you 💬\nType 'quit' to end the conversation.\n\n")
chat_display.configure(state="disabled")

# Input Frame
input_frame = ctk.CTkFrame(app)
input_frame.pack(pady=10)

# User input box
user_input = ctk.CTkEntry(input_frame, width=400, placeholder_text="How are you feeling?")
user_input.pack(side="left", padx=10)

# Function to handle messages
def send_message():
    message = user_input.get()
    if message.strip():
        chat_display.configure(state="normal")
        chat_display.insert("end", f"You: {message}\n")
        response = chatbot_response(message)
        chat_display.insert("end", f"EmpathyBot: {response}\n\n")
        chat_display.configure(state="disabled")
        user_input.delete(0, 'end')
        if message.lower() in ["quit", "exit", "bye"]:
            app.after(1000, app.destroy)
    else:
        messagebox.showwarning("Empty Message", "Please type something before sending.")

# Send button
send_button = ctk.CTkButton(input_frame, text="Send", command=send_message)
send_button.pack(side="right")

# Run the app
app.mainloop()