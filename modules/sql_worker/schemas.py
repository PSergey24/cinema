from typing import Union
from pydantic import BaseModel


class GenreBase(BaseModel):
    movie_id: int
    genre: str

    class Config:
        orm_mode = True


class MovieBase(BaseModel):
    tconst: str
    name: str
    type: str
    year: int
    is_adult: bool
    minutes: Union[int, None] = None
    rating: float
    link: str
    description: str

    # genres: list[GenreBase] = []

    class Config:
        orm_mode = True


class _UserBase(BaseModel):
    login: str


class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True


class User(_UserBase):
    id: int

    class Config:
        orm_mode = True
