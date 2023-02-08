from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from modules.sql_worker import crud
from modules.sql_worker.database import SessionLocal
from modules.models.lstm import made_prediction
from datetime import datetime
import starlette.status as status
import math
from pathlib import Path

app = FastAPI()

# app.mount("/static", StaticFiles(directory=Path(__file__).parent / "modules/web/static"), name="static")
app.mount("/static", StaticFiles(directory="modules/web"), name="static")
templates = Jinja2Templates(directory="modules/web/templates")


@app.get("/")
def read_root():
    return {"Hello": "World2"}


@app.get("/movies", response_class=HTMLResponse)
def show_movies(request: Request):
    db = SessionLocal()

    movies_on_page = 9
    skip = 0

    count_movies = crud.get_count_movies(db=db)
    last_page = math.ceil(count_movies / movies_on_page)

    movies = crud.get_some_movies(db=db, count=movies_on_page, skip=skip)
    return templates.TemplateResponse("movies.html", {"request": request, "movies": movies, "page": 1,
                                                      "last_page": last_page})


@app.get("/movies/pages/{page}", response_class=HTMLResponse)
def show_movies_by_pages(request: Request, page: int):
    db = SessionLocal()

    movies_on_page = 9
    skip = movies_on_page * (page - 1)

    count_movies = crud.get_count_movies(db=db)
    last_page = math.ceil(count_movies / movies_on_page)

    movies = crud.get_some_movies(db=db, count=movies_on_page, skip=skip)
    return templates.TemplateResponse("movies.html", {"request": request, "movies": movies, "page": page,
                                                      "last_page": last_page})


@app.post('/add_comment')
def add_comment(comment: str = Form(...), movie_id: str = Form(...)):
    db = SessionLocal()

    toxic_score = made_prediction([comment])
    crud.create_comment(db=db, movie_id=movie_id, comment=comment, is_toxic=toxic_score, current_time=datetime.now())
    return RedirectResponse(f"/movie/{movie_id}", status_code=status.HTTP_302_FOUND)


@app.get("/movie/{movie_id}", response_class=HTMLResponse)
def show_movie(request: Request, movie_id: int):
    db = SessionLocal()
    movie = crud.get_movie_by_id(db=db, movie_id=movie_id)

    for i, item in enumerate(movie.comments):
        movie.comments[i].is_toxic = round(item.is_toxic, 3)
        movie.comments[i].date_time = item.date_time.strftime('%Y-%m-%d %H:%M:%S')

    return templates.TemplateResponse("item_movie.html", {"request": request, "movie": movie})
