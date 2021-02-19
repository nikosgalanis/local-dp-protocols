import numpy as np
import pandas as pd

path = "ratings.csv"

df = pd.read_csv(path)

df.drop(columns = 'timestamp', inplace = True)

for row in range(len(df)):
    df.iloc[row]['rating'] *= 10

df.head()