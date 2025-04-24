import pandas as pd
df = pd.read_csv('https://huggingface.co/datasets/codewithharsha/LLCP2023/resolve/main/part_01.csv')
df.to_csv('data01.csv', index=False)
print("part 01 CSV file has been saved!!")