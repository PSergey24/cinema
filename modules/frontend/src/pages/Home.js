import React from 'react'
import Header from '../components/Header'
import HomeFirst from '../components/HomeFirst'

class Home extends React.Component{

    render() {
        return(
            <div id="home">
                <Header />
                <HomeFirst />
            </div>
        )
    }
}

export default Home