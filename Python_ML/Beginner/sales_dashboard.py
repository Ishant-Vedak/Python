import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('sales.csv')

sns.scatterplot(data=df, x='Units_Sold', y='Revenue')
plt.show()