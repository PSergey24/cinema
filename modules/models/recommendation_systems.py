import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from ast import literal_eval


# https://www.kaggle.com/code/ibtesama/getting-started-with-a-movie-recommendation-system
def demographic_filtering():
    csv_name = 'data/my_db/movies_4.csv'
    df = pd.read_csv(csv_name, sep='\t', on_bad_lines='skip')

    df_movies = df[df['type'] == 'movie']
    df_series = df[df['type'] == 'tvSeries']

    df_movies = df_movies.dropna(subset=['genres'])
    df_horror = df_movies[df_movies['genres'].str.contains('Horror')]
    df_romance = df_movies[df_movies['genres'].str.contains('Romance')]
    df_comedy = df_movies[df_movies['genres'].str.contains('Comedy')]

    recommendation = get_recommendation(df_movies)
    print(recommendation)
    recommendation = get_recommendation(df_series)
    print(recommendation)
    recommendation = get_recommendation(df_horror)
    print(recommendation)
    recommendation = get_recommendation(df_romance)
    print(recommendation)
    recommendation = get_recommendation(df_comedy)
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


# content-based recommendation
def text_based_recommendation():
    csv_name = 'data/my_db/movies_4.csv'
    df = pd.read_csv(csv_name, sep='\t', on_bad_lines='skip')

    tfidf = TfidfVectorizer(stop_words='english')

    df['description'] = df['description'].fillna('')
    tfidf_matrix = tfidf.fit_transform(df['description'])

    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df.index, index=df['name']).drop_duplicates()
    recommendations = get_content_based_recommendations(df, 'Friends', cosine_sim, indices)
    print(recommendations)
    recommendations = get_content_based_recommendations(df, 'Game of Thrones', cosine_sim, indices)
    print(recommendations)
    recommendations = get_content_based_recommendations(df, 'Serendipity', cosine_sim, indices)
    print(recommendations)


def get_content_based_recommendations(df, title, cosine_sim, indices):
    idx = indices[title]
    if len(df[df['name'] == title]) > 1:
        idx = idx[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return df['name'].iloc[movie_indices]


# actors, directors, keywords, genres
def features_based_recommendation():
    csv_name = 'data/my_db/movies_5.csv'
    df = pd.read_csv(csv_name, sep='\t', on_bad_lines='skip')

    def get_list(names):
        if isinstance(names, list):
            if len(names) > 3:
                names = names[:3]
            return names
        return []

    def clean_data(x):
        if isinstance(x, list):
            return [str.lower(i.replace(" ", "")) for i in x]
        else:
            if isinstance(x, str):
                return str.lower(x.replace(" ", ""))
            else:
                return ''

    def create_soup(x):
        return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])

    def lit_eval(x):
        if isinstance(x, str):
            return literal_eval(x)
        return []

    features = ['cast', 'keywords', 'genres']
    for feature in features:
        df[feature] = df[feature].apply(lit_eval)

    features = ['cast', 'keywords', 'genres']
    for feature in features:
        df[feature] = df[feature].apply(get_list)

    features = ['cast', 'keywords', 'director', 'genres']
    for feature in features:
        df[feature] = df[feature].apply(clean_data)

    df['soup'] = df.apply(create_soup, axis=1)

    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(df['soup'])

    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    indices = pd.Series(df.index, index=df['name'])

    recommendations = get_content_based_recommendations(df, 'Scent of a Woman', cosine_sim, indices)
    print(recommendations)
    recommendations = get_content_based_recommendations(df, 'Friends', cosine_sim, indices)
    print(recommendations)
    recommendations = get_content_based_recommendations(df, 'Office', cosine_sim, indices)
    print(recommendations)
