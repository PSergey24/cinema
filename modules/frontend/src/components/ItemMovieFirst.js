import React, { useContext } from 'react'
import { UserContext } from "../context/UserContext"


const ItemMovieInfo = (props) => {
    const [, , name, , ratings, likes] = useContext(UserContext)

   let is_like = 'False'
   likes.map(function (like) {
        if(like.movie_id == props.id){
            is_like = 'True'
        }
   })

   let is_rating = {'is_exist': 'False', 'rating': 0}
   ratings.map(function (rating) {
        if(rating.movie_id == props.id){
            is_rating['is_exist'] = 'True'
            is_rating['rating'] = rating.rating
        }
   })

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
                        {props.movie.actors.map((actor) => (
                            <span key={actor.id}>{actor.name}, </span>
                        ))}
                        <br /><br />
                        <p>My like to movie: {name ? (is_like == 'True' ? 'like' : 'not like') : 'not logged in'}</p>
                        <p>My rating to movie: {name ? (is_rating['is_exist'] == 'True' ? is_rating['rating'] : 'not value') : 'not logged in'}</p>
                        <br />
                        <p className="description">{props.movie.description}</p>
                    </div>
                </div>
            </div>
        </div>
    )

}

export default ItemMovieInfo