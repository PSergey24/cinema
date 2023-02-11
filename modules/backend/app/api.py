import math
import sys
import json
from datetime import datetime
from fastapi import FastAPI, Body, Form, Request
from fastapi.middleware.cors import CORSMiddleware

sys.path.append(r"/Users/sergey/Applications/Pycharm/PycharmProjects/cinema")
from modules.sql_worker import crud
from modules.sql_worker.database import SessionLocal
from modules.models.lstm import made_prediction


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def read_root():
    return {"message": "Welcome to your todo list. hi!!!"}


@app.get("/movies")
def show_movies():
    db = SessionLocal()

    movies_on_page = 9
    skip = 0

    count_movies = crud.get_count_movies(db=db)
    last_page = math.ceil(count_movies / movies_on_page)

    movies = crud.get_some_movies(db=db, count=movies_on_page, skip=skip)

    return movies


@app.get("/movie/{movie_id}")
def show_movie(movie_id: int):
    db = SessionLocal()
    movie = crud.get_movie_by_id(db=db, movie_id=movie_id)

    for i, item in enumerate(movie.comments):
        movie.comments[i].is_toxic = round(item.is_toxic, 3)
        movie.comments[i].date_time = item.date_time.strftime('%Y-%m-%d %H:%M:%S')
    return movie


@app.post('/add_comment')
def add_comment(data=Body()):
    db = SessionLocal()
    comment = data["body"]["comment"]
    movie_id = data["body"]["movie_id"]
    toxic_score = round(made_prediction([comment]), 3)
    current_time = datetime.now()

    new_comment_id = crud.get_last_comment_id(db) + 1
    crud.create_comment(db=db, movie_id=movie_id, comment=comment, is_toxic=toxic_score, current_time=current_time)

    res = {'id': new_comment_id, 'is_toxic': toxic_score, 'date_time': current_time.strftime('%Y-%m-%d %H:%M:%S')}
    return res
