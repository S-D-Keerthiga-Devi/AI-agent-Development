# 📊 Finance Agent — Intelligent Financial Chatbot

A smart finance assistant that uses large language models and real-time tools to provide insights on stocks, markets, and financial data. Built using Flask and the Agno framework, it intelligently routes queries to either a web agent or a financial agent based on the context.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-API-lightgrey)
![Agno](https://img.shields.io/badge/Powered%20By-Agno-brightgreen)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 🚀 Features

- 🔎 **Web Agent**: Uses DuckDuckGo search to answer general queries with sources.
- 📈 **Finance Agent**: Retrieves real-time stock prices, analyst recommendations, fundamentals, and company info via YFinance.
- 🧠 **Auto Routing**: Automatically sends finance queries to the Finance Agent and others to the Web Agent.
- 🖥️ **Simple UI**: Clean chat interface built with Tailwind CSS.
- 🧾 **Markdown to HTML**: Renders structured financial data beautifully.

---

## 🧠 Tech Stack

- **Python 3.10+**
- **Flask** (backend server)
- **Agno Framework**
  - Groq LLMs (`llama3-70b-8192`)
  - Gemini Pro (optional)
- **DuckDuckGoTools** for news & general info
- **YFinanceTools** for financial data
- **Tailwind CSS** (frontend)
- **HTML + JS** for the chat interface

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/S-D-Keerthiga-Devi/AI-agent-Development.git
cd AI-agent-Development
```

### 2. Create .env File
```bash
Create a .env file in the root with your API keys:
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the App
```bash
python app.py
Then open http://127.0.0.1:5000 in your browser.
```
