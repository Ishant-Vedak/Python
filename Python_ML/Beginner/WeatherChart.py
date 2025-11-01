import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('fake_weather.csv')

for_chicago = df[df['City'] == 'Chicago']['Temperature']
dates_for_chicago = df[df['City'] == 'Chicago']['Date']


for_la = df[df['City'] == 'Los Angeles']['Temperature']
dates_for_la = df[df['City'] == 'Los Angeles']['Date']

for_ny = df[df['City'] == 'New York']['Temperature']
dates_for_ny = df[df['City'] == 'New York']['Date']

c_line = plt.plot(sorted(dates_for_chicago), sorted(for_chicago), 'o-r', label='Chicago')
la_line = plt.plot(sorted(dates_for_la), sorted(for_la), 's-b', label='LA')
ny_line = plt.plot(sorted(dates_for_ny), sorted(for_ny), 's-g', label='NY')
plt.legend()
plt.xlabel('Dates')
plt.ylabel('Temperatures')
plt.show()
