from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from .database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    tconst = Column(String, unique=True, index=True)
    name = Column(String)
    type = Column(String)
    year = Column(Integer)
    is_adult = Column(Boolean)
    minutes = Column(Integer)
    rating = Column(Float)
    link = Column(String)
    description = Column(String)

    genres = relationship("Genre", back_populates="movie_item", lazy="joined")
    comments = relationship("Comment", back_populates="comment_item", lazy="joined")
    actors = relationship("Actor", secondary="actors_movies", back_populates="movies", lazy="joined")


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    genre = Column(String)

    movie_item = relationship("Movie", back_populates="genres")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    comment = Column(String)
    is_toxic = Column(Float)
    date_time = Column(DateTime)

    comment_item = relationship("Movie", back_populates="comments")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    my_likes = relationship("UsersLikes", back_populates="user_item", lazy="joined")
    my_ratings = relationship("UsersRatings", back_populates="user_item", lazy="joined")


class UsersLikes(Base):
    __tablename__ = "users_likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))

    user_item = relationship("User", back_populates="my_likes")


class UsersRatings(Base):
    __tablename__ = "users_ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))
    rating = Column(Float)

    user_item = relationship("User", back_populates="my_ratings")


class Actor(Base):
    __tablename__ = "actors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    birthday = Column(String)
    img = Column(String)

    movies = relationship("Movie", secondary="actors_movies", back_populates="actors", lazy="joined")


class ActorsMovies(Base):
    __tablename__ = "actors_movies"

    movie_id = Column(Integer, ForeignKey("movies.id"), primary_key=True)
    actor_id = Column(Integer, ForeignKey("actors.id"), primary_key=True)
