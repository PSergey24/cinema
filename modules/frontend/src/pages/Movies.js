import React from 'react'
import {useLocation} from 'react-router-dom';
import axios from 'axios'
import Header from '../components/Header'
import MoviesFirst from '../components/MoviesFirst'
import { UserProvider } from "../context/UserContext"


function ContainerMovies() {
	const location = useLocation()
  	return <>
        <Movies way={"http://0.0.0.0:8000" + location.pathname}/>
    </>
}


class Movies extends React.Component{
    constructor(props) {
        super(props)

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
            <UserProvider>
                <div id="movies">
                    <Header />
                    <MoviesFirst moviesList={this.state.movies} current_page={this.state.current_page} last_page={this.state.last_page} />
                </div>
            </UserProvider>
        )
    }
}

export default ContainerMovies