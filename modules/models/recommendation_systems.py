import pandas as pd
import numpy as np


# https://www.kaggle.com/code/ibtesama/getting-started-with-a-movie-recommendation-system
def demographic_filtering():
    csv_name = 'data/my_db/movies_4.csv'
    df = pd.read_csv(csv_name, sep='\t', on_bad_lines='skip')

    df_movies = df[df['type'] == 'movie']
    df_series = df[df['type'] == 'tvSeries']

    recommendation = get_recommendation(df_movies)
    print(recommendation)
    recommendation = get_recommendation(df_series)
    print(recommendation)


def get_recommendation(df):
    C = df['rating'].mean()
    m = df['num_votes'].quantile(0.9)

    def weighted_rating(x, m=m, C=C):
        v = x['num_votes']
        R = x['rating']
        # Calculation based on the IMDB formula
        return (v / (v + m) * R) + (m / (m + v) * C)

    q_movies = df.copy().loc[df['num_votes'] >= m]
    q_movies['score'] = q_movies.apply(weighted_rating, axis=1)
    q_movies = q_movies.sort_values('score', ascending=False)
    return q_movies[['name', 'num_votes', 'rating', 'score']].head(15)



