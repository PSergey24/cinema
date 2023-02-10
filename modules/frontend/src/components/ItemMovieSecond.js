import React from 'react'
import ItemMovieCommentBlock from '../components/ItemMovieCommentBlock'


const ItemMovieSecond = (props) => {

    return(
        <div className="container">
            <div className="row">
                <ItemMovieCommentBlock movie={props.movie} />
                <div className="col-md-6 col-lg-6 similar-movies">
                    <p>similar movies</p>
                </div>
            </div>
        </div>
    )

}

export default ItemMovieSecond