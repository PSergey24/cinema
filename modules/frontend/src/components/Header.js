import React from 'react'

class Header extends React.Component{

    render() {
        return(
            <div className="container-fluid header">
                <div className="container">
                    <div className="row">
                        <div className="col-md-3 col-lg-3">
                            <div className="profile">
                                <ul>
                                    <li><span>My Account</span></li>
                                </ul>
                            </div>
                        </div>
                        <div className="col-md-9 col-lg-9">
                            <div className="navigation">
                                <ul>
                                    <li><a href="/">Home</a></li>
                                    <li><a href="/movies">Movies</a></li>
                                    <li><a href="/#">Categories</a></li>
                                    <li><a href="/#">Recommendation</a></li>
                                    <li><a href="/#">Watched</a></li>
                                    <li><a href="/#">Watch list</a></li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        )
    }
}

export default Header