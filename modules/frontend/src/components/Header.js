import React, { useContext } from 'react'
import { UserContext } from "../context/UserContext"


const Header = () => {
  const [token, setToken] = useContext(UserContext)

  const handleLogout = () => {
    setToken('null')
  }

  return (
    <div className="container-fluid header">
        <div className="container">
            <div className="row">
                <div className="col-md-3 col-lg-3">
                    <div className="profile">
                        <ul>
                            {(token != 'null') ? (
                                <li><button className="button" onClick={handleLogout}>
                                  Logout
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

//function ContainerHeader() {
//	const token = useContext(UserContext)
//  	return <>
//        <Header token={token} />
//    </>
//
//}
//
//class Header extends React.Component{
//    constructor(props){
//         super(props)
//         this.state = {
//            token: this.props.token
//         }
//
//         this.handleLogout = this.handleLogout.bind(this)
//    }
//
//    handleLogout(){
//        this.setState(null)
//    }
//
//    render() {
//        return(
//            <div className="container-fluid header">
//                <div className="container">
//                    <div className="row">
//                        <div className="col-md-3 col-lg-3">
//                            <div className="profile">
//                                <ul>
//                                    {this.state.token ? (
//                                        <li><button className="button" onClick={this.handleLogout}>
//                                          Logout
//                                        </button></li>
//                                    ) : (
//                                        <li><span>Who are you?</span></li>
//                                    )}
//                                </ul>
//                            </div>
//                        </div>
//                        <div className="col-md-9 col-lg-9">
//                            <div className="navigation">
//                                <ul>
//                                    <li><a href="/">Home</a></li>
//                                    <li><a href="/movies">Movies</a></li>
//                                    <li><a href="/#">Categories</a></li>
//                                    <li><a href="/#">Recommendation</a></li>
//                                    <li><a href="/#">Watched</a></li>
//                                    <li><a href="/#">Watch list</a></li>
//                                </ul>
//                            </div>
//                        </div>
//                    </div>
//                </div>
//            </div>
//        )
//    }
//}
//
//export default ContainerHeader