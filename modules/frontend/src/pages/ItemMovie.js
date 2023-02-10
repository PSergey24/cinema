import React, {useState, useEffect} from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import Header from '../components/Header'
import ItemMovieInfo from '../components/ItemMovieInfo'
import ItemMovieSecond from '../components/ItemMovieSecond'


export default function ItemMovie() {
    let params =  useParams()
    let movieId = params.id
    const [movie, setMovie] = React.useState(null)

    useEffect(() => {
        axios.get(`http://0.0.0.0:8000/movie/${movieId}`).then((response) => {
            setMovie(response.data);
        })
    }, [])

    if (!movie) return null;

    return (
        <div id="movie">
            <Header />
            <ItemMovieInfo movie={movie} />
            <ItemMovieSecond movie={movie} />
        </div>
    )
}