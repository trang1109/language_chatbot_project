from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
import spacy
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Hugging Face model (sử dụng GPT hoặc bất kỳ mô hình nào khác từ Hugging Face)
model = pipeline("text-generation", model="gpt2")

# Rasa URL
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    # Phân tích ý định và thực thể bằng spaCy (NLP)
    doc = nlp(user_message)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Tích hợp Rasa cho xử lý intent
    rasa_response = requests.post(RASA_SERVER_URL, json={"sender": "user", "message": user_message})
    rasa_data = rasa_response.json()

    # Gửi câu hỏi tới mô hình Hugging Face GPT-2 để sinh câu trả lời
    response = model(user_message, max_length=50, num_return_sequences=1, truncation=True)
    gpt_reply = response[0]['generated_text'].strip()

    # Trả lại câu trả lời
    return jsonify({"reply": gpt_reply, "rasa_intent": rasa_data})

if __name__ == '__main__':
    app.run(debug=True)
