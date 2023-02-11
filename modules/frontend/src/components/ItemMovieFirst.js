import React from 'react'


const ItemMovieInfo = (props) => {

    return(
        <div className="container">
            <div className="row">
                <div className="col-md-3 col-lg-3">
                    <div className="container-left">
                        <figure className="img-item-movie">
                            <img src={props.movie.link} alt={props.movie.name} />
                            <h5 id="movie_name">{props.movie.name}</h5>
                            <p id="movie_year">{props.movie.year}</p>
                        </figure>
                    </div>
                </div>
                <div className="col-md-9 col-lg-9">
                    <div className="container-right">
                        <p className="actors">Actors: </p>
                        <p className="description">{props.movie.description}</p>
                    </div>
                </div>
            </div>
        </div>
    )

}

export default ItemMovieInfo