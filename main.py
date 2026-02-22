import os
import requests
import pandas as pd
import time
from serpapi import GoogleSearch
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("SERPAPI_KEY")

if not API_KEY:
    raise ValueError("SERPAPI_KEY not found in .env file")

# Create image folder
os.makedirs("input_image", exist_ok=True)

data = []
image_count = 580
target_images = 3000

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

        image_url = img.get("original") or img.get("thumbnail")
        caption = img.get("title")

        if not image_url or not caption:
            continue

        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(image_url, headers=headers, timeout=5)

            if response.status_code == 200:
                image_path = f"input_image/img_{image_count}.jpg"

                with open(image_path, "wb") as f:
                    f.write(response.content)

                data.append({
                    "image_path": image_path,
                    "caption": caption
                })

                image_count += 1
                print("Downloaded:", image_count)

        except Exception as e:
            print("Skipped:", e)

# Save CSV as data.csv
df = pd.DataFrame(data)
df.to_csv("data.csv", index=False)

print("\nDataset created with", len(df), "images.")