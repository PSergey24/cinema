import React, { useContext, useState } from "react"
import axios from 'axios'
import { UserContext } from "../context/UserContext"
import ErrorMessage from "../components/ErrorMessage"


const Login = () => {
    const [login, setLogin] = useState("")
    const [password, setPassword] = useState("")
    const [errorMessage, setErrorMessage] = useState("")
    const [, setToken] = useContext(UserContext)

    const submitLogin = () => {
        const requestOptions = {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: { login: login, hashed_password: password },
        }


        console.log(requestOptions)
        axios.post(`http://0.0.0.0:8000/api/token`, requestOptions).then((response) => {
            if (response.statusText != 'OK') {
                setErrorMessage(response.data.detail)
            } else {
                setToken(response.data.access_token)
            }
        })
    }

    const handleSubmit = (e) => {
        e.preventDefault()
        submitLogin()
    }

    return (
        <div className="authorization">
            <form onSubmit={handleSubmit}>
                <h1>Authentication</h1>
                <input type="text" placeholder="Enter login" id="login-auth" value={login} onChange={(e) => setLogin(e.target.value)} required />
                <input type="password" placeholder="Enter Password" id="psw-auth" value={password} onChange={(e) => setPassword(e.target.value)} required />
                <ErrorMessage message={errorMessage} />
                <p><button type="submit" className="submit">Login</button></p>
            </form>
        </div>
    )
}

export default Login