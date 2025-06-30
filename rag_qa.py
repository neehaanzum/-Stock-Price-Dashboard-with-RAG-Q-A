import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# Configure your Google API key directly (or via environment variable if needed)
genai.configure(api_key="AIzaSyB_5Gwe2Tu_V7yftt9DdZXj0UJ47KXX8cQ")  # Replace this line with st.secrets or env if needed

model = genai.GenerativeModel("gemini-pro")

def scrape_news(query):
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}&tbm=nws"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for item in soup.select("a"):
        href = item.get("href")
        title = item.text.strip()
        if href and "/url?q=" in href and title:
            clean_url = href.split("/url?q=")[1].split("&")[0]
            results.append((title, clean_url))
            if len(results) == 3:
                break
    return results

def summarize_article(link):
    try:
        response = requests.get(link, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs[:10])  # First 10 paragraphs

        prompt = f"Summarize this article content:\n{text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing: {e}"
