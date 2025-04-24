import pandas as pd
df = pd.read_csv('https://huggingface.co/datasets/codewithharsha/LLCP2023/resolve/main/part_02.csv')
df.to_csv('data02.csv', index=False)
print("part 02 CSV file has been saved!!")