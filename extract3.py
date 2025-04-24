import pandas as pd
df = pd.read_csv('https://huggingface.co/datasets/codewithharsha/LLCP2023/resolve/main/part_03.csv')
df.to_csv('data03.csv', index=False)
print("part 03 CSV file has been saved!!")