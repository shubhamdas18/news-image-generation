import os
import requests
import pandas as pd
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY")

if not API_KEY:
    raise ValueError("SERPAPI_KEY not found in .env file")

#print("API KEY:", API_KEY)


# Create images folder
os.makedirs("images", exist_ok=True)

data = []
image_count = 0
target_images = 1000

# News-related queries
queries = [
    "India politics",
    "India economy",
    "India sports",
    "India technology",
    "India weather",
    "India education",
    "India healthcare",
    "India railway",
    "India business",
    "India elections"
]

for query in queries:
    if image_count >= target_images:
        break

    print(f"Searching for: {query}")

    params = {
        "engine": "google_images",
        "q": query + " news",
        "api_key": API_KEY,
        "num": 100
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    images_results = results.get("images_results", [])

    for img in images_results:
        if image_count >= target_images:
            break

        image_url = img.get("original")
        caption = img.get("title")

        if not image_url or not caption:
            continue

        try:
            response = requests.get(image_url, timeout=5)
            if response.status_code == 200:
                image_path = f"images/img_{image_count}.jpg"

                with open(image_path, "wb") as f:
                    f.write(response.content)

                data.append({
                    "image_path": image_path,
                    "caption": caption
                })

                image_count += 1
                print("Downloaded:", image_count)

        except Exception as e:
            print("Skipped image:", e)
            continue

# Save dataset
df = pd.DataFrame(data)
df.to_csv("news_dataset_%t.csv"%(), index=False)

print("\nDataset created with", len(df), "images.")
