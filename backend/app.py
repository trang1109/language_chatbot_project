from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import spacy
import requests

app = Flask(__name__)
CORS(app)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# OpenAI GPT API key
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="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",
)

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

    # Gửi câu hỏi tới GPT-3.5 để sinh câu trả lời
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_message}
        ],
        max_tokens=150
    )
    gpt_reply = response['choices'][0]['message'].content.strip()

    # Trả lại câu trả lời
    return jsonify({"reply": gpt_reply, "rasa_intent": rasa_data})

if __name__ == '__main__':
    app.run(debug=True)
