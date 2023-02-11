import React from 'react'
import HomeRegistrationForm from '../components/HomeRegistrationForm'


class HomeFirst extends React.Component{

    render() {
        return(
            <div className="container">
                <div className="row">
                    <div className="col-md-4 col-lg-4 offset-4">
                        <HomeRegistrationForm />
                    </div>
                </div>
            </div>
        )
    }
}

export default HomeFirst