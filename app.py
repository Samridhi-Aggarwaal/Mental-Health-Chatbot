#Flask-based chatbot web app, pretrained neural network

import os
import json
import nltk                                         #NLP
import pickle                                       #Load preprocessed data
import random
import numpy as np
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model      #Load the trained deep learning model
from nltk.tokenize import TreebankWordTokenizer
from flask import Flask, render_template, request   #Run a web server and serve chatbot responses

# Setup custom nltk_data directory
nltk_data_dir = os.path.join(os.getcwd(), 'nltk_data')
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.append(nltk_data_dir)
nltk.download('wordnet', download_dir=nltk_data_dir)
nltk.download('omw-1.4', download_dir=nltk_data_dir)

# Initialize preprocessing tools
lemmatizer = WordNetLemmatizer()
tokenizer = TreebankWordTokenizer()

# Load chatbot data and model
model = load_model('model.h5')
words = pickle.load(open('texts.pkl', 'rb'))
classes = pickle.load(open('labels.pkl', 'rb'))
with open('intents.json', encoding='utf-8') as f:
    intents = json.load(f)

# Create Flask app
app = Flask(__name__)

#Helper Functions
# Tokenize and lemmatize the sentence
def clean_up_sentence(sentence):
    sentence_words = tokenizer.tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Convert sentence into bag-of-words array
def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print(f"Found in bag: {w}")
    return np.array(bag)

# Predict intent based on input
def predict_class(sentence):
    p = bow(sentence, words, show_details=False)
    print("Input shape to model:", np.array([p]).shape)
    print("Model input expected shape:", model.input_shape)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

# Get response from intents JSON
def get_response(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

#Flask web app
# Define home route for chatbot UI
@app.route("/")
def index():
    return render_template("index.html")



# Define route for chatbot API
from google.cloud import translate_v2 as translate
import os

# Make sure this environment variable points to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "E:/STUDY/EmpathyBot/Mental-Health-Chatbot/keys/plucky-rarity-457710-f8-60878cfa5552.json"

translate_client = translate.Client()

def detect_language(text):
    result = translate_client.detect_language(text)
    return result['language']

def translate_text(text, target_language='en'):
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']


from flask import request
from langdetect import detect
from google.cloud import translate_v2 as translate

translate_client = translate.Client()

@app.route("/get", methods=["GET", "POST"])
def chatbot_response():
    try:
        msg = request.values.get("msg")
        lang = request.values.get("lang", "en")  # default to English
        if not msg:
            return "No message received."

        print(f"User message ({lang}): {msg}")
        # Translate input to English
        translated_input = translate_client.translate(msg, target_language='en', source_language=lang)['translatedText']
        ints = predict_class(translated_input)
        if not ints:
            return "I'm not sure how to respond to that."

        res = get_response(ints, intents)

        # Translate bot response to user’s selected language
        translated_output = translate_client.translate(res, target_language=lang)['translatedText']
        return translated_output

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Server error: {str(e)}"

# Define test route
@app.route("/test")
def test():
    return "Server is up and running!"

#Run app
if __name__ == "__main__":
    app.run(debug=True)
