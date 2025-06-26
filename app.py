import corpora
import streamlit as st
import requests
from textblob import TextBlob
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
import nltk

nltk.download("punkt")

# Load .env API key
load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

# Page config
st.set_page_config(page_title="Finance Sentiment Analyzer", layout="centered")

# Styling
st.markdown(
    """
    <style>
    .stTitle { color: #0066cc; }
    .stSubtitle { font-size: 18px; color: #333333; margin-top: -16px; }
    </style>
""",
    unsafe_allow_html=True,
)

# App title
st.title("Finance News Sentiment Analyzer")
st.markdown(
    "<div class='stSubtitle'>Analyze the tone of financial headlines in real time</div>",
    unsafe_allow_html=True,
)

# User input
ticker = st.text_input("Enter stock ticker (e.g. AAPL, TSLA)").upper()


# Get news
def get_news(ticker):
    url = f"https://newsapi.org/v2/everything?q={ticker}&apiKey={API_KEY}&pageSize=10&sortBy=publishedAt"
    response = requests.get(url)
    return response.json()


# Analyze sentiment
def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "🟢 Positive"
    elif polarity < -0.1:
        return "🔴 Negative"
    else:
        return "🟡 Neutral"


# Sentiment label mapping for pie chart
chart_labels = {
    "🟢 Positive": "Positive",
    "🔴 Negative": "Negative",
    "🟡 Neutral": "Neutral",
}

# Main logic
if ticker:
    with st.spinner("Fetching news and analyzing sentiment..."):
        news_data = get_news(ticker)

    if news_data["status"] == "ok":
        sentiments = {"🟢 Positive": 0, "🔴 Negative": 0, "🟡 Neutral": 0}
        st.subheader(f"Headlines for **{ticker}**")

        for article in news_data["articles"]:
            title = article["title"]
            sentiment = analyze_sentiment(title)
            sentiments[sentiment] += 1
            st.markdown(
                f"- **{title}**<br>_Sentiment: {sentiment}_", unsafe_allow_html=True
            )

        # Pie chart
        fig, ax = plt.subplots()
        colors = ["#2ecc71", "#e74c3c", "#f1c40f"]  # green, red, yellow
        ax.pie(
            sentiments.values(),
            labels=[chart_labels[label] for label in sentiments.keys()],
            autopct="%1.1f%%",
            colors=colors,
            textprops={"fontsize": 12},
        )
        ax.set_title("Sentiment Breakdown", fontsize=16)
        st.pyplot(fig)
    else:
        st.error("❌ Failed to fetch news. Please check the ticker or API key.")
