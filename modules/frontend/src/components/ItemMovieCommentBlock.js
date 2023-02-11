import React from 'react'
import axios from 'axios'
import ItemMovieAddComment from '../components/ItemMovieAddComment'
import ItemMovieComments from '../components/ItemMovieComments'


class ItemMovieCommentBlock extends React.Component{
    constructor(props){
         super(props)
         this.state = {
            comments: props.movie.comments
         }

         this.AddComment = this.AddComment.bind(this)
    }

    render(){
        return(
            <div className="col-md-6 col-lg-6">
                <div className="row">
                    <ItemMovieAddComment movie_id={this.props.movie.id} onAdd={this.AddComment} />
                    <ItemMovieComments comments={this.state.comments} />
                </div>
            </div>
        )
    }

    AddComment(comment){
        const requestOptions = {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: comment,
        }

        axios.post(`http://0.0.0.0:8000/add_comment`, requestOptions).then((response) => {
            const id = response.data.id
            const is_toxic = response.data.is_toxic
            const date_time = response.data.date_time
            this.setState({comments: [...this.state.comments, {id, is_toxic, date_time, ...comment}]})
        })
    }
}

export default ItemMovieCommentBlock