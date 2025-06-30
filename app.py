import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
from datetime import date
from prophet import Prophet
from prophet.plot import plot_plotly
import pandas as pd
import ta
from io import BytesIO
from rag_qa import scrape_news, summarize_article  # Using Gemini now

# ---------------- CONFIG ----------------
st.set_page_config(page_title="📈 Stock Price Dashboard", layout="wide")
st.title("📈 Stock Price Dashboard with RAG Q&A")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Select Stock & Period")

ticker_options = {
    "Apple (AAPL)": "AAPL", "Google (GOOGL)": "GOOGL", "Microsoft (MSFT)": "MSFT",
    "Amazon (AMZN)": "AMZN", "Tesla (TSLA)": "TSLA", "Meta (META)": "META",
    "TCS (India)": "TCS.NS", "Infosys (India)": "INFY.NS",
    "Reliance (India)": "RELIANCE.NS", "HDFC Bank (India)": "HDFCBANK.NS",
    "Nifty 50 (Index)": "^NSEI", "Sensex (Index)": "^BSESN",
    "S&P 500 (Index)": "^GSPC", "Dow Jones (Index)": "^DJI", "Nasdaq 100 (Index)": "^NDX"
}

selected_company = st.sidebar.selectbox("Choose Stock or Index", list(ticker_options.keys()))
ticker = ticker_options[selected_company]

custom_ticker = st.sidebar.text_input("Or enter a custom ticker (optional)")
if custom_ticker:
    ticker = custom_ticker.upper()

start_date = st.sidebar.date_input("Start Date", date(2023, 1, 1))
end_date = st.sidebar.date_input("End Date", date.today())

# Toggles
show_forecast = st.sidebar.checkbox("Show 30-Day Forecast (Prophet)")
show_rsi = st.sidebar.checkbox("Show RSI")
show_macd = st.sidebar.checkbox("Show MACD")

# ---------------- MAIN SECTION ----------------
if ticker:
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)

        if data.empty:
            st.error("⚠️ No data found for this ticker and date range.")
        else:
            st.subheader(f"📈 Closing Price: {ticker}")
            st.line_chart(data['Close'])

            st.subheader("🔍 Candlestick Chart")
            fig = go.Figure(data=[go.Candlestick(
                x=data.index, open=data['Open'], high=data['High'],
                low=data['Low'], close=data['Close']
            )])
            fig.update_layout(xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

            # Download buttons
            csv = data.to_csv().encode()
            st.download_button("📅 Download Data (CSV)", csv, f"{ticker}_data.csv", "text/csv")

            buf = BytesIO()
            fig.write_image(buf, format="png")
            st.download_button("📷 Download Chart (PNG)", buf.getvalue(), f"{ticker}_chart.png", "image/png")

            # RSI
            if show_rsi:
                st.subheader("📊 RSI - Relative Strength Index")
                rsi = ta.momentum.RSIIndicator(close=data['Close']).rsi()
                st.line_chart(rsi)

            # MACD
            if show_macd:
                st.subheader("📊 MACD - Moving Average Convergence Divergence")
                macd = ta.trend.MACD(data['Close'])
                macd_df = pd.DataFrame({
                    "MACD": macd.macd(),
                    "Signal": macd.macd_signal()
                })
                st.line_chart(macd_df)

            # Forecast
            if show_forecast:
                st.subheader("🔮 Forecast using Prophet (30 Days)")
                df = data.reset_index()[['Date', 'Close']]
                df['Date'] = df['Date'].dt.tz_localize(None)
                df.rename(columns={"Date": "ds", "Close": "y"}, inplace=True)

                model = Prophet()
                model.fit(df)

                future = model.make_future_dataframe(periods=30)
                forecast = model.predict(future)

                forecast_plot = plot_plotly(model, forecast)
                st.plotly_chart(forecast_plot, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")

# ---------------- RAG Q&A SECTION ----------------
st.markdown("---")
st.header("💬 Ask the AI about your stock")

user_query = st.text_input("Ask a question (e.g., 'Latest news about Tesla')", "")

if user_query:
    st.write("🔎 Searching and summarizing...")
    try:
        links = scrape_news(user_query)
        if not links:
            st.warning("No relevant articles found.")
        else:
            for title, link in links:
                st.subheader(f"📰 {title}")
                st.markdown(f"[Read full article]({link})")
                summary = summarize_article(link)
                st.markdown(f"**AI Summary:** {summary}")
                st.markdown("---")
    except Exception as e:
        st.error(f"❌ Something went wrong during Q&A: {e}")
