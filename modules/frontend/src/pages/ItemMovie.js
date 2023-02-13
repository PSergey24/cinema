import React, {useEffect} from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import Header from '../components/Header'
import ItemMovieFirst from '../components/ItemMovieFirst'
import ItemMovieSecond from '../components/ItemMovieSecond'
import { UserProvider } from "../context/UserContext"


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
        <UserProvider>
            <div id="movie">
                <Header />
                <ItemMovieFirst movie={movie} />
                <ItemMovieSecond movie={movie} />
            </div>
        </UserProvider>
    )
}