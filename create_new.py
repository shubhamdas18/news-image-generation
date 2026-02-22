import os
import time
import requests
import pandas as pd
from newspaper import Article
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def serpapi_google_news(query, api_key, num=50):
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google_news",
        "q": query,
        "api_key": api_key,
        "num": num
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


API_KEY = os.getenv("SERPAPI_KEY")
IMAGE_DIR = "/content/images"
CSV_PATH = "/content/news_dataset.csv"

TARGET_IMAGES = 10000
SAVE_EVERY = 20
SLEEP = 1.0

os.makedirs(IMAGE_DIR, exist_ok=True)

queries = [
    "India politics", "India economy", "India sports",
    "India technology", "India education", "India healthcare",
    "India business", "India elections"
]

headers = {"User-Agent": "Mozilla/5.0"}

data = []
seen_images = set()
image_count = 0

vectorizer = TfidfVectorizer(stop_words="english")

def similarity(a, b):
    if not a or not b:
        return 0.0
    tfidf = vectorizer.fit_transform([a, b])
    return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]

for query in queries:
    if image_count >= TARGET_IMAGES:
        break

    print(f"\n🔍 Query: {query}")
    results = serpapi_google_news(query, API_KEY)
    news_results = results.get("news_results", [])

    for news in news_results:
        if image_count >= TARGET_IMAGES:
            break

        url = news.get("link")
        snippet = news.get("snippet", "")  

        if not url:
            continue

        try:
            article = Article(url)
            article.download()
            article.parse()

            if not article.text:
                del article
                continue

            highlight = article.text.strip().split("\n")[0]
            if len(highlight) < 60:
                del article
                continue

            image_url = article.top_image or news.get("thumbnail")
            if not image_url or image_url in seen_images:
                del article
                continue

            sim = similarity(snippet, highlight)

            img_path = f"{IMAGE_DIR}/img_{image_count}.jpg"
            r = requests.get(image_url, headers=headers, timeout=10)
            if r.status_code != 200:
                del article
                continue

            with open(img_path, "wb") as f:
                f.write(r.content)

            data.append({
                "image_path": img_path,
                "snippet": snippet,
                "highlight": highlight,
                "similarity_score": round(sim, 3)
            })

            seen_images.add(image_url)
            image_count += 1
            print(f" Saved {image_count}")

            if image_count % SAVE_EVERY == 0:
                pd.DataFrame(data).to_csv(CSV_PATH, index=False)

            del article
            time.sleep(SLEEP)

        except Exception as e:
            print(" Skipped:", e)

pd.DataFrame(data).to_csv(CSV_PATH, index=False)

print("\n DONE!")
print(f" Samples saved: {len(data)}")