Mood Journal App

A simple mood health and wellbeing application that helps users track their emotions over time using journaling + AI-powered sentiment analysis.

🚀 Features

📓 Daily journaling with mood tracking

🤖 Sentiment analysis powered by Hugging Face models

📊 Visual charts of emotional trends over time (Chart.js)

🔐 Environment variable support via .env

🛠️ Tech Stack

Frontend: HTML5, CSS, JavaScript (Chart.js)

Backend: Python (Flask)

Database: MySQL

📂 Project Setup
1. Clone the repository
git clone https://github.com/your-username/mood-journal.git
cd mood-journal

2. Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Setup environment variables

Create a .env file in the project root:

# Flask
FLASK_ENV=development
FLASK_SECRET=super-secret-key
PORT=5000

# MySQL
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=mood_journal

# Hugging Face
HF_API_KEY=hf_your_api_key_here
HF_MODEL=j-hartmann/emotion-english-distilroberta-base
⚠Remember to add .env to your .gitignore.

▶Run the app
flask run


App will be available at: http://127.0.0.1:5000/

 Database Setup (MySQL)

Login to MySQL and create the database:

CREATE DATABASE mood_journal;


Update your .env file with your MySQL user and password.

📜 License

MIT License
