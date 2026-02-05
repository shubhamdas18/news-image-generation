import pandas as pd
import re

def clean_caption(text):
    if pd.isna(text):
        return "Indian news image"

    text = str(text)

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # Remove text after separators
    text = re.split(r'\||-|–|—|:', text)[0]

    # Remove special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # Fallback caption
    if len(text) < 3:
        text = "Indian news image"

    return text

# Load existing dataset
df = pd.read_csv("news_dataset.csv")

# Clean captions
df["caption"] = df["caption"].apply(clean_caption)

# Save cleaned dataset
df.to_csv("news_dataset_clean.csv", index=False)

print("Cleaned CSV saved as news_dataset_clean.csv")
