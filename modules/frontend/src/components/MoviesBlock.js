import React from 'react'
import MoviesList from '../components/MoviesList'

class MoviesBlock extends React.Component{

    render() {
        return(
            <div class="container">
                <div class="row">
                    <div class="col-md-9 col-lg-9">
                        <MoviesList moviesList={this.props.moviesList} />
                    </div>
                    <div class="col-md-3 col-lg-3">

                    </div>
                </div>
            </div>
        )
    }
}

export default MoviesBlock