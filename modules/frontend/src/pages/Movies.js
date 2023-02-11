import React, {useState, useEffect} from 'react'
import {useLocation} from 'react-router-dom';
import axios from 'axios'
import Header from '../components/Header'
import MoviesBlock from '../components/MoviesBlock'
import MoviesPages from '../components/MoviesPages'


function ContainerMovies() {
	const location = useLocation()
	console.log(location.pathname)
  	return <>
        <Movies way={"http://0.0.0.0:8000" + location.pathname}/>
    </>
}


class Movies extends React.Component{
    constructor(props) {
        super(props)
        console.log(this.props.way)
        axios.get(this.props.way).then((res) => {
            this.setState({movies: res.data.movies, current_page: res.data.current_page, last_page: res.data.last_page})
        })

        this.state = {
            movies: [],
            current_page: null,
            last_page: null
        }
    }

    render() {
        return(
            <div id="movies">
                <Header />
                <MoviesBlock moviesList={this.state.movies} />
                <MoviesPages current_page={this.state.current_page} last_page={this.state.last_page} />
            </div>
        )
    }
}

export default ContainerMovies