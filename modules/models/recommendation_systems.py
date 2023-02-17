import pandas as pd
import numpy as np
from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from ast import literal_eval


# https://www.kaggle.com/code/ibtesama/getting-started-with-a-movie-recommendation-system
# https://www.kaggle.com/code/rounakbanik/movie-recommender-systems
# https://www.kaggle.com/code/fabiendaniel/film-recommendation-engine
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


def collaborative_filtration():
    reader = Reader()
    csv_ratings = 'data/kaggle_movie_dataset/ratings.csv'
    ratings = pd.read_csv(csv_ratings, on_bad_lines='skip')
    csv_name = 'data/my_db/movies_5.csv'
    df = pd.read_csv(csv_name, sep='\t', on_bad_lines='skip')
    ratings = ratings.iloc[:3000000]
    ratings = ratings.drop(columns=['timestamp'])
    ratings = add_rating(ratings)

    data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

    svd = SVD()
    cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

    trainset = data.build_full_trainset()
    svd.fit(trainset)

    def predict(user_id, movie):
        prediction = svd.predict(user_id, movie['id_kaggle_ds'], 3)
        return prediction.est

    prediction = svd.predict(1, 302, 3)
    print(f'test result: {prediction}')

    df['CF_rating'] = df.apply(lambda row: predict(1000000, row), axis=1)
    rec = df.sort_values(by='CF_rating', ascending=False, na_position='first')
    print(rec[0:11].loc[:, ['name', 'CF_rating', 'rating']])


def add_rating(df_ratings):
    # Saw, Serendipity, Interstellar, The Martian, Scream, The Fault in Our Stars, Se7en,
    # Hidden Figures, About Time, The Theory of Everything, Step Up, Cube, The Lord of the Rings, Whiplash,
    # Scent of a Woman, Knockin' on Heaven's Door, Titanic
    my = {176: 5, 9778: 4, 157336: 5, 286217: 4.5, 4232: 5, 381219: 4.5, 807: 4.5, 381284: 5, 122906: 4.5, 266856: 4.5,
          9762: 4, 431: 4, 123: 3, 367412: 3, 9475: 5, 158: 4, 597: 4.5}
    list_rating = []
    for key, value in my.items():
        d = {'userId': 1000000, 'movieId': key, 'rating': value}
        list_rating.append(d)
    df = pd.DataFrame(list_rating)
    df_ratings = pd.concat([df_ratings, df], ignore_index=True)
    return df_ratings
