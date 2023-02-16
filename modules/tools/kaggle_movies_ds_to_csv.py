import pandas as pd
import numpy as np
import math
import re
import json
from datetime import datetime

# https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset


def fix_bugs():
    kaggle_movies_metadata = 'data/kaggle_movie_dataset/movies_metadata.csv'
    df_movies_metadata = pd.read_csv(kaggle_movies_metadata, on_bad_lines='skip')
    df_movies_metadata = df_movies_metadata.drop([35585])
    df_movies_metadata.to_csv(kaggle_movies_metadata, index=False)


# update IMDB db
def kaggle_actors_db_to_csv():
    kaggle_credits = 'data/kaggle_movie_dataset/credits.csv'
    df_credits = pd.read_csv(kaggle_credits, on_bad_lines='skip')

    kaggle_movies_metadata = 'data/kaggle_movie_dataset/movies_metadata.csv'
    df_movies_metadata = pd.read_csv(kaggle_movies_metadata, on_bad_lines='skip')

    df_movies_metadata["id"] = pd.to_numeric(df_movies_metadata["id"])
    df_union = pd.merge(df_credits, df_movies_metadata, on="id")

    my_db = 'data/my_db/movies_3.csv'
    df_my_db = pd.read_csv(my_db, sep='\t', on_bad_lines='skip')

    df_actors = pd.DataFrame(columns=['id', 'name'])
    df_actors_movies = pd.DataFrame(columns=['id', 'movie_id', 'actor_id'])

    index_actor_movies = 1
    for i, row in df_my_db.iterrows():
        movie = df_union.loc[df_union['imdb_id'] == row['tconst']]

        if len(movie) == 0:
            continue

        casters = get_casters(re.findall(r'\{.*?\}', movie.iloc[0]['cast']))
        # crews = get_crews(re.findall(r'\{.*?\}', movie['crew'].item()))

        list_actors = []
        list_actors_movies = []
        for caster_id, caster in casters.items():
            d = {'id': index_actor_movies, 'movie_id': row['id'], 'actor_id': caster_id}
            list_actors_movies.append(d)

            index_actor_movies += 1
            actor = df_actors.loc[df_actors['id'] == caster_id]
            if len(actor) > 0:
                continue

            d2 = {'id': caster_id, 'name': caster, 'birthday': '', 'img': ''}
            list_actors.append(d2)

        df = pd.DataFrame(list_actors_movies)
        df_actors_movies = pd.concat([df_actors_movies, df], ignore_index=True)

        df = pd.DataFrame(list_actors)
        df_actors = pd.concat([df_actors, df], ignore_index=True)
        print(f'{row["id"]}: {row["name"]}')

    df_actors.to_csv('data/my_db/actors.csv', index=False, sep='\t')
    df_actors_movies.to_csv('data/my_db/actors_movies.csv', index=False, sep='\t')


def get_casters(items):
    casters = {}
    for item in items:
        try:
            cast_id, name = get_caster(item)
            casters.update({cast_id: name})
        except:
            print(f"Exception get_caster: {item}")
    return casters


def get_caster(item):
    cast_id = re.findall(r'\d+', re.findall(r'\'id\': \d*', item)[0])[0]
    name = re.findall(r'[\'\"]{1}name[\'\"]{1}[^,]*', item)[0].split(': ')[1][1:-1]
    return cast_id, name


def get_crews(items):
    crews = {}
    for item in items:
        crew_id = re.findall(r'\d+', re.findall(r'\'id\': \d*', item)[0])[0]
        name = re.findall(r'name[^,]*', item)[0].split(': ')[1][1:-1]
        job = re.findall(r'job[^,]*', item)[0].split(': ')[1][1:-1]
        crews.update({crew_id: [name, job]})
    return crews


def kaggle_rating_db_to_csv():
    my_db = 'data/my_db/movies_3.csv'
    df_my_db = pd.read_csv(my_db, sep='\t', on_bad_lines='skip')

    kaggle_movies_metadata = 'data/kaggle_movie_dataset/movies_metadata.csv'
    df_movies_metadata = pd.read_csv(kaggle_movies_metadata, on_bad_lines='skip')

    kaggle_ratings = 'data/kaggle_movie_dataset/ratings.csv'
    df_ratings = pd.read_csv(kaggle_ratings, on_bad_lines='skip')

    df_users = pd.DataFrame(columns=['id', 'login', 'password'])
    df_users_ratings = pd.DataFrame(columns=['id', 'user_id', 'movie_id', 'rating'])
    df_users_likes = pd.DataFrame(columns=['id', 'user_id', 'movie_id'])

    list_users_ratings = []
    list_users_likes = []
    index_ratings = 1
    index_likes = 1
    for i, row in df_ratings.iterrows():
        if i > 5000000:
            break

        item = df_movies_metadata.loc[df_movies_metadata['id'] == row['movieId']]

        user = df_users.loc[df_users['id'] == row['userId']]
        if len(user) == 0:
            d = {'id': int(row['userId']), 'login': f"login_{int(row['userId'])}", 'password': f"login_{int(row['userId'])}"}
            df = pd.DataFrame([d])
            df_users = pd.concat([df_users, df], ignore_index=True)

        if i % 50000 == 0:
            print(f'processed {i} rows, {datetime.now().strftime("%H:%M:%S")}')

        if len(item) == 0:
            continue

        movie = df_my_db.loc[df_my_db['tconst'] == item.iloc[0]['imdb_id']]

        try:
            d = {'id': index_ratings, 'user_id': int(row['userId']), 'movie_id': int(movie['id']), 'rating': row['rating']}
            list_users_ratings.append(d)
            index_ratings += 1
        except:
            print(f'Problem with index_ratings={index_ratings}')

        if row['rating'] < 5:
            continue

        try:
            d = {'id': index_likes, 'user_id': int(row['userId']), 'movie_id': int(movie['id'])}
            list_users_likes.append(d)
            index_likes += 1
        except:
            print(f'Problem with index_likes={index_ratings}')

    df = pd.DataFrame(list_users_ratings)
    df_users_ratings = pd.concat([df_users_ratings, df], ignore_index=True)

    df = pd.DataFrame(list_users_likes)
    df_users_likes = pd.concat([df_users_likes, df], ignore_index=True)

    df_users_ratings.to_csv('data/my_db/users_ratings.csv', index=False, sep='\t')
    df_users_likes.to_csv('data/my_db/users_likes.csv', index=False, sep='\t')
    df_users.to_csv('data/my_db/users.csv', index=False, sep='\t')


def update_info_kaggle_mdb_to_imdb():
    my_db = 'data/my_db/movies.csv'

    kaggle_movies_metadata = 'data/kaggle_movie_dataset/movies_metadata.csv'
    df_movies_metadata = pd.read_csv(kaggle_movies_metadata, on_bad_lines='skip')

    df_my_db = pd.read_csv(my_db, sep='\t', on_bad_lines='skip')

    for i, row in df_my_db.iterrows():

        movie = df_movies_metadata.loc[df_movies_metadata['imdb_id'] == row['tconst']]
        if len(movie) == 0:
            continue

        df_my_db.loc[i, 'description'] = movie.iloc[0]['overview']
        print(f'{i}: {movie.iloc[0]["title"]} - updated')
    df_my_db.to_csv('data/my_db/movies_2.csv', index=False, sep='\t')


def kaggle_movies_db_to_csv():
    my_db = 'data/my_db/movies_2.csv'

    kaggle_movies_metadata = 'data/kaggle_movie_dataset/movies_metadata.csv'
    df_movies_metadata = pd.read_csv(kaggle_movies_metadata, on_bad_lines='skip')

    df_my_db = pd.read_csv(my_db, sep='\t', on_bad_lines='skip')

    index = len(df_my_db)
    for i, row in df_movies_metadata.iterrows():
        if len(df_my_db.loc[df_my_db['tconst'] == row['imdb_id']]) > 0:
            continue

        year = row['release_date'].split('-')[0] if isinstance(row['runtime'], str) is True else ''
        is_adult = 1 if row['adult'] is True else 0

        d = {'id': index, 'tconst': row['imdb_id'], 'name': row['title'], 'year': year, 'isAdult': is_adult,
             'minutes': int(row['runtime']) if math.isnan(row['runtime']) is not True else '',
             'genres': get_genres(row['genres']) if isinstance(row['genres'], str) is True else '',
             'type': 'movie',
             'rating': row['vote_average'] if math.isnan(row['vote_average']) is not True else '',
             'linkImg': '',
             'description': row['overview'] if isinstance(row['overview'], str) is True else ''}

        df = pd.DataFrame([d])
        df_my_db = pd.concat([df_my_db, df], ignore_index=True)
        print(f'{index} / {len(df_movies_metadata)}: {row["title"]} - added')

        index += 1
    df_my_db.to_csv('data/my_db/movies_3.csv', index=False, sep='\t')


def get_genres(input_genres):
    genres = ''

    data = input_genres.split('}')

    for i in range(len(data) - 1):
        name = data[i].split("\'name\': ")[1].replace('\'', '')
        genres += name
        if i < len(data) - 2:
            genres += ', '
    return genres

