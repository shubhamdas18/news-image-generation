import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from newspaper import Article
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -------------------- LOAD ENV --------------------
load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY")

if not API_KEY:
    raise ValueError("SERPAPI_KEY not found. Check your .env file.")

# -------------------- PATH SETUP --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images_final")
CSV_PATH = os.path.join(BASE_DIR, "text_image_dataset.csv")

os.makedirs(IMAGE_DIR, exist_ok=True)

# -------------------- CONFIG --------------------
TARGET_IMAGES = 1500
SAVE_EVERY = 5
SLEEP = 1.0

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


# -------------------- FUNCTIONS --------------------
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


def similarity(a, b):
    if not a or not b:
        return 0.0
    tfidf = vectorizer.fit_transform([a, b])
    return cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]


# -------------------- MAIN LOOP --------------------
for query in queries:
    if image_count >= TARGET_IMAGES:
        break

    print(f"\n🔍 Query: {query}")

    try:
        results = serpapi_google_news(query, API_KEY)
    except Exception as e:
        print("❌ API Error:", e)
        continue

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
                continue

            highlight = article.text.strip().split("\n")[0]

            if len(highlight) < 60:
                continue

            image_url = article.top_image or news.get("thumbnail")

            if not image_url or image_url in seen_images:
                continue

            sim = similarity(snippet, highlight)

            img_path = os.path.join(IMAGE_DIR, f"img_{image_count}.jpg")

            r = requests.get(image_url, headers=headers, timeout=10)
            if r.status_code != 200:
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

            print(f"✅ Saved {image_count}")

            if image_count % SAVE_EVERY == 0:
                pd.DataFrame(data).to_csv(CSV_PATH, index=False)

            time.sleep(SLEEP)

        except Exception as e:
            print("⚠️ Skipped:", e)


# -------------------- FINAL SAVE --------------------
pd.DataFrame(data).to_csv(CSV_PATH, index=False)

print("\n🎉 DONE!")
print(f"Total Samples Saved: {len(data)}")