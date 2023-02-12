import React from 'react'
import Header from '../components/Header'
import HomeFirst from '../components/HomeFirst'
import { UserProvider } from "../context/UserContext"

class Home extends React.Component{

    render() {
        return(
            <UserProvider>
                <div id="home">
                    <Header />
                    <HomeFirst />
                </div>
            </UserProvider>
        )
    }
}

export default Home