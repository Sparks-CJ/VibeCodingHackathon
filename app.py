from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import requests
from intasend import APIService

app = Flask(__name__)
CORS(app)  # Allow frontend JS requests

# ----------------------
# Database Config
# ----------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",        # change if needed
    password="",        # change if needed
    database="mood_db"  # make sure this DB exists
)
cursor = db.cursor()

# ----------------------
# Hugging Face Sentiment Analysis
# ----------------------
HF_API_URL = "https://api-inference.huggingface.co/models/nlptown/bert-base-multilingual-uncased-sentiment"
HF_HEADERS = {"Authorization": "Bearer YOUR_HUGGINGFACE_API_KEY"}

def analyze_sentiment(text):
    res = requests.post(HF_API_URL, headers=HF_HEADERS, json={"inputs": text})
    if res.status_code == 200:
        return res.json()
    return {"error": "Sentiment analysis failed"}

# ----------------------
# IntaSend Setup
# ----------------------
intasend = APIService(
    publishable_key="YOUR_INTASEND_PUBLISHABLE_KEY",
    secret_key="YOUR_INTASEND_SECRET_KEY",
    test=True  # switch to False in production
)

# ----------------------
# Routes
# ----------------------

@app.route("/journal", methods=["POST"])
def save_journal():
    data = request.json
    entry = data.get("entry")

    # Sentiment analysis
    sentiment = analyze_sentiment(entry)

    # Extract a score or label
    sentiment_label = str(sentiment)

    # Save to DB
    cursor.execute("INSERT INTO journals (entry, sentiment) VALUES (%s, %s)", (entry, sentiment_label))
    db.commit()

    return jsonify({"message": "Journal saved", "sentiment": sentiment})

@app.route("/journal", methods=["GET"])
def get_journals():
    cursor.execute("SELECT id, entry, sentiment, created_at FROM journals ORDER BY created_at DESC")
    rows = cursor.fetchall()

    journals = []
    for r in rows:
        journals.append({
            "id": r[0],
            "entry": r[1],
            "sentiment": r[2],
            "created_at": r[3].strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify(journals)

# ----------------------
# Payment Routes
# ----------------------

@app.route("/pay", methods=["POST"])
def initiate_payment():
    data = request.json
    amount = data.get("amount", 200)  # default KES 200
    phone_number = data.get("phone_number")

    res = intasend.collection.mpesa_stk_push(phone_number, amount, "Mood Journal Premium")
    
    return jsonify(res)

@app.route("/pay/status/<checkout_id>", methods=["GET"])
def check_status(checkout_id):
    res = intasend.collection.get_status(checkout_id)
    return jsonify(res)
    import os
app.config['MYSQL_HOST'] = os.environ.get("MYSQL_HOST")
app.config['MYSQL_USER'] = os.environ.get("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.environ.get("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.environ.get("MYSQL_DATABASE")


# ----------------------
# Run App
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)
