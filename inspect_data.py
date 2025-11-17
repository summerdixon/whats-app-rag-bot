from datasets import load_dataset
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Name of the dataset you want to view
# Example: "wikitext", "google/fleurs", or your private repo "username/dataset"
DATASET_ID = "AAOOCambodia/KhmerSmot01" 
CONFIG_NAME = "None" # Some datasets have sub-configs, otherwise set to None

# 2. Load only the first few items (Streaming mode)
print(f"🔍 Connecting to {DATASET_ID}...")
ds = load_dataset(DATASET_ID, CONFIG_NAME, split="train", streaming=True)

# 3. Print the structure and first 3 rows
print("\n--- DATA STRUCTURE ---")
# Note: In streaming mode, .features isn't always available immediately, 
# so we infer it from the first item.
first_item = next(iter(ds))
print(f"Columns detected: {list(first_item.keys())}")

print("\n--- FIRST 3 EXAMPLES ---")
for i, item in enumerate(ds.take(3)):
    print(f"\nRow {i+1}:")
    print(item)

print("\n------------------------")
print("✅ Inspection complete. No huge files downloaded.")