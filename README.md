# 📈 Stock Price Dashboard with RAG Q&A (Powered by Google Gemini)

This project is a powerful **Streamlit web app** that enables users to:

- 📊 View historical stock data and technical indicators  
- 🔮 Predict future trends using **Facebook Prophet**
- 📉 Visualize with candlestick charts and download data
- 🧠 Ask questions about stock-related news using **RAG (Retrieval-Augmented Generation)** and **Google Gemini (PaLM)**

---

## 🔧 Features

- ✅ Interactive stock selection (NASDAQ, Indian stocks, Indices)
- ✅ Candlestick chart, MACD, RSI, and CSV download
- ✅ 30-day forecasting using Prophet
- ✅ RAG Q&A with **Google Generative AI**
- ✅ Automatically fetches and summarizes stock-related news

---

## 📁 File Structure

    Stock_Price_Dashboard/
    ├── app.py # Main Streamlit app
    ├── rag_qa.py # RAG module using Google Gemini API
    ├── requirements.txt # Python dependencies

## 🚀 Demo

    App Demo:
## ⚙️ Setup Instructions

### 1. Clone the repository

      git clone https://github.com/neehaanzum/-Stock-Price-Dashboard-with-RAG-Q-A.git

2. Install dependencies

        pip install -r requirements.txt

3. Add your Google API Key

Open rag_qa.py and replace the placeholder:

      genai.configure(api_key="YOUR_GOOGLE_API_KEY")

▶️ Run the app

      streamlit run app.py
