import React from 'react'
import MoviesItem from '../components/MoviesItem'

class MoviesList extends React.Component{

    render() {
        return(
            <div className="row">
                {this.props.moviesList.map((movie) => (
                    <MoviesItem id={movie.id} name={movie.name} link={movie.link} />
                ))}
            </div>
        )
    }
}

export default MoviesList