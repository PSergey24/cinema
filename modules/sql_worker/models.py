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

    genres = relationship("Genre", back_populates="movie_item")
    comments = relationship("Comment", back_populates="comment_item")


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
