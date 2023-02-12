import React from 'react'
import Register from '../components/Register'
import Login from '../components/Login'

class HomeRegistrationForm extends React.Component{

    render() {
        return(
            <div className="form">
                <Register />
                <Login />
            </div>
        )
    }
}

export default HomeRegistrationForm