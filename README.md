# 📋 WhatsApp To-Do Extractor (Regex-based)

This project extracts actionable to-do tasks from WhatsApp `.txt` chats using smart Regex patterns and instruction keywords. It identifies whether a task is for the sender ("me") or the recipient.

## 🚀 Features

- Upload `.txt` WhatsApp chat exports
- Extract tasks using Regex and keyword logic
- Distinguish sender vs receiver responsibilities
- View tasks on UI
- Download extracted tasks as JSON

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python (Flask)
- **Other**: Regex, Flask-CORS, DeepSeek API (optional for smart inference)


## 🧪 How It Works

1. Upload your WhatsApp `.txt` file.
2. Regex identifies actionable lines (based on verbs like "buy", "send", "remind", etc.).
3. Tasks are categorized as sender/receiver responsibilities.
4. Download your todo list as JSON.

## ▶️ Running Locally

1. Clone the repo:
git clone https://github.com/prince1823/wp_1.git

Run the Flask backend:  cd backend

pip install -r requirements.txt

python app.py

3. Open `frontend/index.html` in your browser.

## 📄 License

This project is licensed under the MIT License.


