import React from 'react'


const ItemMovieCommentForm = (props) => {

    return(
        <div className="col-md-12 col-lg-12 container-add-comment">
            <form method="post" action="/add_comment">
                <textarea id="comment" name="comment" rows="5"></textarea>
                <input type="hidden" id="movie_id" name="movie_id" value={props.movie_id} />
                <p><input class="submit" type="submit" value="comment" /></p>
            </form>
        </div>
    )

}

export default ItemMovieCommentForm