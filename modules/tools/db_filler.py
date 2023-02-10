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


def movies_csv_to_db():
    db = SessionLocal()
    df = pd.read_csv('data/movies_2.csv', sep='\t', on_bad_lines='skip')
    df = df.replace(['\\N'], None)

    index_movie = crud.get_last_movie_id(db=db)

    for i, row in df.iterrows():
        genres_list = row['genres'].lower().replace(' ', '').split(',')

        movie = create_movie(row)
        genres = create_genres(genres_list, index_movie)
        crud.create_movie(db=db, movie=movie)
        crud.create_genres(db=db, genres=genres)
        print(f'{i}/{len(df)}, {row["name"]}')
        index_movie += 1


def create_movie(row):
    return schemas.MovieBase(tconst=row['tconst'], name=row['name'], type=row['type'], year=row['year'],
                             is_adult=row['isAdult'], minutes=row['minutes'], rating=row['rating'],
                             link=row['linkImg'], description=row['description'])


def create_genres(genres_list, movie_id):
    return [create_genre(genre, movie_id) for genre in genres_list]


def create_genre(genre, movie_id):
    return schemas.GenreBase(genre=genre, movie_id=movie_id)


# extract data
def get_movies():
    db = SessionLocal()
    movies = crud.get_movies(db)
    return movies


def get_genres():
    db = SessionLocal()
    genres = crud.get_genres(db)
    return genres
