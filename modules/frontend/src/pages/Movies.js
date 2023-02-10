import React, {useState, useEffect} from 'react'
import axios from 'axios'
import Header from '../components/Header'
import MoviesBlock from '../components/MoviesBlock'
import MoviesPages from '../components/MoviesPages'

class Movies extends React.Component{
    constructor(props) {
        super(props)

        axios.get('http://0.0.0.0:8000/movies').then((res) => {
            this.setState({movies: res.data})
        })

        this.state = {
            movies: []
        }
    }

    render() {
        return(
            <div id="movies">
                <Header />
                <MoviesBlock moviesList={this.state.movies} />
                <MoviesPages />
            </div>
        )
    }
}

//const Movies = () => {
//    let [movies, setMovies] = useState([])
//
//    useEffect(() => {
//        getMovies()
//    }, [])
//
//    let getMovies = async () => {
//        let response = await fetch('http://0.0.0.0:8000/movies')
//        let data = await response.json()
//        setMovies(data)
//    }
//
//    return(
//        <div id="movies">
//            <Header />
//            <MoviesBlock moviesList={movies} />
//        </div>
//    )
//
//}

export default Movies