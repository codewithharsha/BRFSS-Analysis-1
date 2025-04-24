import pandas as pd
import os

# Read the XPT file
df = pd.read_sas('/content/drive/MyDrive/LLCP2023.XPT ', format='xport')

# Number of splits
num_parts = 3

# Create output directory if needed
output_dir = "/content/Splits"
os.makedirs(output_dir, exist_ok=True)

# Split and save
chunk_size = len(df) // num_parts

for i in range(num_parts):
    start = i * chunk_size
    end = (i + 1) * chunk_size if i < num_parts - 1 else len(df)
    chunk = df.iloc[start:end]
    output_path = os.path.join(output_dir, f"part_{i+1}.csv")
    chunk.to_csv(output_path, index=False)
    print(f"Saved {output_path} with {len(chunk)} rows")
