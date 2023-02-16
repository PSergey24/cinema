import pandas as pd
from modules.sql_worker import models, schemas, crud
from modules.sql_worker.database import SessionLocal, engine


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def db_creator():
    models.Base.metadata.create_all(bind=engine)


def csv_to_db():
    db_creator()

    db = SessionLocal()

    movies_csv_to_db(db)
    actors_csv_to_db(db)
    users_csv_to_db(db)
    users_ratings_csv_to_db(db)
    users_likes_csv_to_db(db)
    actors_movies_csv_to_db(db)


def movies_csv_to_db(db):
    df = pd.read_csv('data/my_db/movies.csv', sep='\t', on_bad_lines='skip')
    df = df.replace(['\\N'], None)

    index_movie = crud.get_last_movie_id(db=db)

    for i, row in df.iterrows():
        genres_list = row['genres'].lower().replace(' ', '').split(',')

        movie = create_movie(row)
        genres = create_genres(genres_list, index_movie)
        crud.create_genres(db=db, genres=genres)
        crud.create_movie(db=db, movie=movie)

        if index_movie % 1000 == 0:
            print(f'movies: {i}/{len(df)}')

        if index_movie == 3100:
            break

        index_movie += 1
    print('Movies were uploaded from csv to db')


def create_movie(row):
    return schemas.MovieBase(tconst=row['tconst'], name=row['name'], type=row['type'], year=row['year'],
                             is_adult=row['isAdult'], minutes=row['minutes'], rating=row['rating'],
                             link=row['linkImg'], description=row['description'])


def create_genres(genres_list, movie_id):
    return [create_genre(genre, movie_id) for genre in genres_list]


def create_genre(genre, movie_id):
    return schemas.GenreBase(genre=genre, movie_id=movie_id)


def actors_csv_to_db(db):
    df = pd.read_csv('data/my_db/actors.csv', sep='\t', on_bad_lines='skip')

    for i, row in df.iterrows():
        crud.create_actor(db=db, actor=row)

        if i % 10000 == 0:
            print(f'actors: {i}/{len(df)}')
    print('Actors were uploaded from csv to db')


def actors_movies_csv_to_db(db):
    df = pd.read_csv('data/my_db/actors_movies.csv', sep='\t', on_bad_lines='skip')

    for i, row in df.iterrows():
        crud.create_actors_movies(db=db, item=row)

        if i % 10000 == 0:
            print(f'actors_movies: {i}/{len(df)}')
    print('ActorsMovies were uploaded from csv to db')


def users_csv_to_db(db):
    df = pd.read_csv('data/my_db/users.csv', sep='\t', on_bad_lines='skip')

    for i, row in df.iterrows():
        crud.create_login(db=db, user=row)

        if i == 100:
            break
    print('Users were uploaded from csv to db')


def users_ratings_csv_to_db(db):
    df = pd.read_csv('data/my_db/users_ratings.csv', sep='\t', on_bad_lines='skip')

    for i, row in df.iterrows():
        crud.create_users_ratings(db=db, item=row)

        if i % 10000 == 0:
            print(f'users_ratings: {i}/{len(df)}')
    print('UsersRatings were uploaded from csv to db')


def users_likes_csv_to_db(db):
    df = pd.read_csv('data/my_db/users_likes.csv', sep='\t', on_bad_lines='skip')

    for i, row in df.iterrows():
        crud.create_users_likes(db=db, item=row)

        if i % 10000 == 0:
            print(f'users_likes: {i}/{len(df)}')
    print('UsersLikes were uploaded from csv to db')


# extract data
def get_movies():
    db = SessionLocal()
    movies = crud.get_movies(db)
    return movies


def get_genres():
    db = SessionLocal()
    genres = crud.get_genres(db)
    return genres


def get_comments():
    db = SessionLocal()
    comments = crud.get_comments(db)
    return comments


def get_users():
    db = SessionLocal()
    comments = crud.get_users(db)
    return comments
