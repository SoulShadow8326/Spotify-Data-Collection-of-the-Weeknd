import pandas as pd
import matplotlib.pyplot as plt
import os

if not os.path.exists('plots'):
    os.makedirs('plots')

artists = pd.read_csv('data/artists.csv')
albums = pd.read_csv('data/albums.csv')
tracks = pd.read_csv('data/all_tracks.csv')

albums['Release Year'] = pd.to_datetime(albums['Release Date']).dt.year
popularity_trend = albums.groupby('Release Year')['Name'].count().reset_index()
popularity_trend.rename(columns={"Name": "Number of Albums"}, inplace=True)

plt.figure(figsize=(10, 6))
plt.plot(popularity_trend['Release Year'], popularity_trend['Number of Albums'], marker='o', label="Albums Released")
plt.title("Albums Released Over Time")
plt.xlabel("Year")
plt.ylabel("Number of Albums")
plt.grid()
plt.legend()
plt.savefig('plots/popularity_trend.png', transparent=True) 
plt.close()

genres = artists['Genres'][0].split(", ")
genre_counts = pd.Series(genres).value_counts()

genre_counts.plot(kind='pie', autopct='%1.1f%%', figsize=(8, 8), title="Artist's Genre Distribution")
plt.ylabel("")
plt.savefig('plots/genre_distribution.png', transparent=True) 
plt.close()

explicit_counts = tracks['Explicit'].value_counts()

explicit_counts.plot(kind='bar', color=['green', 'red'], figsize=(6, 4))
plt.title("Explicit vs. Clean Tracks")
plt.xlabel("Explicit Content")
plt.ylabel("Number of Tracks")
plt.xticks(ticks=[0, 1], labels=['Clean', 'Explicit'], rotation=0)
plt.savefig('plots/explicit_vs_clean.png', transparent=True) 
plt.close()

tracks['Duration (minutes)'] = tracks['Duration (ms)'] / 60000

tracks['Duration (minutes)'].hist(bins=20, color='skyblue', edgecolor='black', figsize=(8, 6))
plt.title("Distribution of Track Durations")
plt.xlabel("Duration (minutes)")
plt.ylabel("Number of Tracks")
plt.savefig('plots/track_duration_distribution.png', transparent=True)  
plt.close()

print("Analysis Complete!")
print("Plots have been saved in the 'plots' folder:")
print("1. Popularity Trend: plots/popularity_trend.png")
print("2. Genre Distribution: plots/genre_distribution.png")
print("3. Explicit vs. Clean Tracks: plots/explicit_vs_clean.png")
print("4. Track Duration Distribution: plots/track_duration_distribution.png")