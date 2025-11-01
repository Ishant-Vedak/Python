import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('imdb_top_1000.csv')
df['Genre'] = df['Genre'].str.split(',')
df_exploded = df.explode('Genre')
avg_ratings = df_exploded.groupby('Genre')['IMDB_Rating'].mean().sort_values(ascending=False)
plt.bar(avg_ratings.index, avg_ratings.values)
plt.xlabel('Genres')
plt.ylabel('Mean Ratings')
plt.show()

