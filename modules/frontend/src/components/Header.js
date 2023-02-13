import React, { useContext } from 'react'
import { UserContext } from "../context/UserContext"


const Header = () => {
  const [token, setToken, name, setName] = useContext(UserContext)

  const handleLogout = () => {
    setToken('null')
    setName(null)
  }

  return (
    <div className="container-fluid header">
        <div className="container">
            <div className="row">
                <div className="col-md-3 col-lg-3">
                    <div className="profile">
                        <ul>
                            {name ? (
                                <li><button className="button" onClick={handleLogout}>
                                  Logout - {name}
                                </button></li>
                            ) : (
                                <li><span>Who are you?</span></li>
                            )}
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

export default Header
