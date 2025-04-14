import os
import json
import nltk
import pickle
import random
import numpy as np
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
from nltk.tokenize import TreebankWordTokenizer
from flask import Flask, render_template, request

# Setup custom nltk_data directory
nltk_data_dir = os.path.join(os.getcwd(), 'nltk_data')
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.append(nltk_data_dir)

# Force download resources
nltk.download('wordnet', download_dir=nltk_data_dir)
nltk.download('omw-1.4', download_dir=nltk_data_dir)

# Initialize preprocessing tools
lemmatizer = WordNetLemmatizer()
tokenizer = TreebankWordTokenizer()

# Load chatbot data and model
model = load_model('model.h5')
words = pickle.load(open('texts.pkl', 'rb'))
classes = pickle.load(open('labels.pkl', 'rb'))
intents = json.loads(open('intents.json').read())

# Create Flask app
app = Flask(__name__)

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

# Define route for chatbot UI
@app.route("/")
def index():
    return render_template("index.html")

# Define route for chatbot API
@app.route("/get", methods=["GET", "POST"])
def chatbot_response():
    try:
        msg = request.values.get("msg")  # works for both GET and POST
        if not msg:
            return "No message received."
        print(f"User message: {msg}")
        ints = predict_class(msg)
        print(f"Predicted intents: {ints}")
        if not ints:
            return "I'm not sure how to respond to that."
        res = get_response(ints, intents)
        print(f"Bot response: {res}")
        return res
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Server error: {str(e)}"

# Test route
@app.route("/test")
def test():
    return "Server is up and running!"

if __name__ == "__main__":
    app.run(debug=True)
