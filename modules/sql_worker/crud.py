from sqlalchemy.orm import Session
from sqlalchemy import desc

from . import models, schemas


def create_movie(db: Session, movie):
    db_movie = models.Movie(tconst=movie.tconst, name=movie.name, type=movie.type, year=movie.year,
                            is_adult=movie.is_adult, minutes=movie.minutes, rating=movie.rating,
                            link=movie.link, description=movie.description)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)


def create_genres(db: Session, genres):
    genres_model = create_genre_models(genres)
    db.add_all(genres_model)
    db.commit()
    for item in genres_model:
        db.refresh(item)


def create_genre_models(genres):
    return [models.Genre(movie_id=item.movie_id, genre=item.genre) for item in genres]


def create_comment(db: Session, movie_id, comment, is_toxic, current_time):
    db_comment = models.Comment(movie_id=movie_id, comment=comment, is_toxic=is_toxic, date_time=current_time)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)


def get_movies(db: Session):
    return db.query(models.Movie).all()


def get_some_movies(db: Session, count=9, skip=0):
    return db.query(models.Movie).offset(skip).limit(count).all()


def get_movie_by_id(db: Session, movie_id):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


def get_count_movies(db: Session):
    return db.query(models.Movie).count()


def get_genres(db: Session):
    return db.query(models.Genre).all()


def get_last_movie_id(db: Session):
    last_movie = db.query(models.Movie).order_by(desc(models.Movie.id)).limit(1).all()
    if len(last_movie) == 0:
        return 1
    return last_movie[0].id + 1
