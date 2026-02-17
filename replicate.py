import pandas as pd

# Load existing dataset
df = pd.read_csv("news_dataset_clean.csv")

# Number of times to replicate
replications = 15

# Repeat the dataset
df_replicated = pd.concat([df] * replications, ignore_index=True)

# Save new CSV
df_replicated.to_csv("news_dataset_final.csv", index=False)

print("New dataset created with", len(df_replicated), "rows.")
