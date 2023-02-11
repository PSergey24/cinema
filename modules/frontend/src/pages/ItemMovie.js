import React, {useEffect} from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import Header from '../components/Header'
import ItemMovieFirst from '../components/ItemMovieFirst'
import ItemMovieSecond from '../components/ItemMovieSecond'


export default function ItemMovie() {
    let params =  useParams()
    let movieId = params.id
    const [movie, setMovie] = React.useState(null)

    useEffect(() => {
        axios.get(`http://0.0.0.0:8000/movie/${movieId}`).then((response) => {
            setMovie(response.data);
        })
    }, [movieId])

    if (!movie) return null;

    return (
        <div id="movie">
            <Header />
            <ItemMovieFirst movie={movie} />
            <ItemMovieSecond movie={movie} />
        </div>
    )
}