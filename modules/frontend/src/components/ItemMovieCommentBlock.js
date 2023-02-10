import React from 'react'
import ItemMovieCommentForm from '../components/ItemMovieCommentForm'
import ItemMovieComments from '../components/ItemMovieComments'


const ItemMovieCommentBlock = (props) => {

    return(
        <div className="col-md-6 col-lg-6">
            <div className="row">
                <ItemMovieCommentForm movie_id={props.movie.id} />
                <ItemMovieComments comments={props.movie.comments} />
            </div>
        </div>
    )

}

export default ItemMovieCommentBlock