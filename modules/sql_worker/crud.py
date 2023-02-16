from sqlalchemy.orm import Session
from sqlalchemy import desc
from modules.sql_worker import models
from modules.sql_worker import schemas as _schemas
import fastapi as _fastapi
import fastapi.security as _security
import sqlalchemy.orm as _orm
import passlib.hash as _hash
import jwt as _jwt


oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")
JWT_SECRET = "myjwtsecret"


def get_user_by_login(login: str, db):
    return db.query(models.User).filter(models.User.login == login).first()


def create_user(user: _schemas.UserCreate, db):
    user_obj = models.User(
        login=user.login, hashed_password=user.hashed_password
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj


def authenticate_user(login: str, password: str, db):
    user = get_user_by_login(db=db, login=login)

    if not user:
        return False

    if password == user.hashed_password:
        return user
    return False


def create_token(user: models.User):
    user_obj = _schemas.User.from_orm(user)
    token = _jwt.encode(user_obj.dict(), JWT_SECRET)
    return dict(access_token=token, token_type="bearer")


def get_current_user(db, token):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )
    return user


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


def get_last_comment_id(db: Session):
    last_comment = db.query(models.Comment).order_by(desc(models.Comment.id)).limit(1).all()
    if len(last_comment) == 0:
        return 0
    return last_comment[0].id


def create_comment(db: Session, movie_id, comment, is_toxic, current_time):
    db_comment = models.Comment(movie_id=movie_id, comment=comment, is_toxic=is_toxic, date_time=current_time)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)


def create_actor(db: Session, actor):
    db_movie = models.Actor(id=int(actor['id']), name=actor['name'], birthday=actor['birthday'], img=actor['img'])
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)


def create_actors_movies(db: Session, item):
    db_movie = models.ActorsMovies(actor_id=int(item['actor_id']), movie_id=int(item['movie_id']))
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)


def create_login(db: Session, user):
    db_movie = models.User(id=int(user['id']), login=user['login'], hashed_password=user['password'])
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)


def create_users_likes(db: Session, item):
    db_movie = models.UsersLikes(id=int(item['id']), user_id=int(item['user_id']), movie_id=int(item['movie_id']))
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)


def create_users_ratings(db: Session, item):
    db_movie = models.UsersRatings(id=int(item['id']), user_id=int(item['user_id']), movie_id=int(item['movie_id']),
                                   rating=float(item['rating']))
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)


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


def get_comments(db: Session):
    return db.query(models.Comment).all()


def get_users(db: Session):
    return db.query(models.User).all()


def get_last_movie_id(db: Session):
    last_movie = db.query(models.Movie).order_by(desc(models.Movie.id)).limit(1).all()
    if len(last_movie) == 0:
        return 1
    return last_movie[0].id + 1
