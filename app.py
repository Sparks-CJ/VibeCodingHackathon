from flask import Flask, render_template, request, jsonify
import mysql.connector
import requests
import os

app = Flask(__name__)

# MySQL Config
db_config = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
    "database": os.getenv("MYSQL_DB", "moodjournal")
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Hugging Face API
HF_API_URL = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"
HF_API_KEY = os.getenv("HF_API_KEY")
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

# IntaSend API
INTASEND_API_KEY = os.getenv("INTASEND_API_KEY")
INTASEND_URL = "https://payment.intasend.com/api/v1/checkout/"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/add_entry', methods=['POST'])
def add_entry():
    content = request.json.get("content", "")
    if not content:
        return jsonify({"error": "Empty journal entry"}), 400

    # Sentiment analysis
    response = requests.post(HF_API_URL, headers=headers, json={"inputs": content})
    result = response.json()
    sentiment, score = "neutral", 0.0
    if isinstance(result, list) and len(result) > 0:
        label_data = result[0][0]
        sentiment = label_data['label']
        score = float(label_data['score'])

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO entries(content, sentiment, score) VALUES(%s, %s, %s)",
        (content, sentiment, score)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Entry saved!", "sentiment": sentiment, "score": score})

@app.route('/get_entries')
def get_entries():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, content, sentiment, score, created_at FROM entries ORDER BY created_at DESC")
    entries = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(entries)

@app.route('/pay', methods=['POST'])
def pay():
    data = request.json
    amount = data.get("amount", 1)
    email = data.get("email", "test@example.com")

    payload = {
        "public_key": INTASEND_API_KEY,
        "amount": amount,
        "currency": "KES",
        "email": email,
        "redirect_url": "https://yourapp.onrender.com"
    }

    resp = requests.post(INTASEND_URL, json=payload)
    return jsonify(resp.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


