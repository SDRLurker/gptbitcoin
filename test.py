import os
from dotenv import load_dotenv
import requests

load_dotenv()

def get_bitcoin_news():
    serpapi_key = os.getenv("SERPAPI_API_KEY")
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_news",
        "q": "btc",
        "api_key": serpapi_key
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status ()
        data = response. json()
        news_results = data.get("news_results", [])
        headlines = []
        for item in news_results:
            headlines.append({
                "title": item.get("title", ""),
                "date": item.get("date", "")
            })
        return headlines[:5] # 최신 5개의 뉴스 헤드라인만 반환
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

print(get_bitcoin_news())