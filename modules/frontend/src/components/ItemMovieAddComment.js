import React from 'react'


class ItemMovieAddComment extends React.Component{
    constructor(props){
         super(props)
         this.state = {
            comment: "",
            movie_id: props.movie_id
         }
    }

    render(){
        return(
            <div className="col-md-12 col-lg-12 container-add-comment">
                <form>
                    <textarea id="comment" name="comment" rows="5" onChange={(e) => this.setState({comment:e.target.value})}></textarea>
                    <input type="hidden" id="movie_id" name="movie_id" value={this.props.movie_id} />
                    <p><input class="submit" type="button" value="comment" onClick={() => this.props.onAdd({
                        comment: this.state.comment,
                        movie_id: this.state.movie_id
                    })} /></p>
                </form>
            </div>
        )
    }
}

export default ItemMovieAddComment