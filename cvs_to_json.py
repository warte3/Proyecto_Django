import pandas as pd
import json

df = pd.read_csv('peliculas_dataset.csv')

df.to_json('peliculas.json', orient='records')

with open('peliculas.json','r') as file:
    movies = json.load(file)


for i in range(100):
    movie = movies[i]
    print(movie)
    break