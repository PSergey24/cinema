import React from 'react'


class ItemMovieComments extends React.Component{

    render(){
        return(
            <div className="col-md-12 col-lg-12 container-comments">
                {this.props.comments.map((comment) => (
                    <div className={comment.is_toxic < 0.3 ? 'item-comment-bad' : comment.is_toxic > 0.7 ? 'item-comment-good' : 'item-comment'} key={comment.id}>
                        <p className="comment">{comment.comment}</p>
                        <p>
                            <span className="author">Nickname, </span>
                            <span className="toxic_score">{comment.is_toxic}, </span>
                            <span className="comment_date">{comment.date_time}</span>
                        </p>
                    </div>
                ))}
            </div>
        )
    }
}

export default ItemMovieComments