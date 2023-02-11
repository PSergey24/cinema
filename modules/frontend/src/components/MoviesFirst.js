import React from 'react'
import MoviesList from '../components/MoviesList'
import MoviesPages from '../components/MoviesPages'

class MoviesBlock extends React.Component{

    render() {
        return(
            <div className="container">
                <div className="row">
                    <div className="col-md-9 col-lg-9">
                        <MoviesList moviesList={this.props.moviesList} />
                    </div>
                    <div className="col-md-3 col-lg-3">

                    </div>
                </div>
                <div className="row">
                    <MoviesPages current_page={this.props.current_page} last_page={this.props.last_page} />
                </div>
            </div>
        )
    }
}

export default MoviesBlock