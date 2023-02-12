import React, { useContext, useState } from "react"
import axios from 'axios'
import { UserContext } from "../context/UserContext"
import ErrorMessage from "../components/ErrorMessage"


const Register = () => {
  const [login, setLogin] = useState("")
  const [password, setPassword] = useState("")
  const [confirmationPassword, setConfirmationPassword] = useState("")
  const [errorMessage, setErrorMessage] = useState("")
  const [, setToken] = useContext(UserContext)

  const submitRegistration = () => {
    const requestOptions = {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: { login: login, hashed_password: password },
//      body: JSON.stringify({ login: login, hashed_password: password }),
    }

    console.log(requestOptions)
//    const response = fetch("/api/users", requestOptions);
//    const data = response.json();
//
//    console.log(response)
//    console.log(data)
//    if (!response.ok) {
//      setErrorMessage(data.detail);
//    } else {
//      setToken(data.access_token);
//    }
    axios.post(`http://0.0.0.0:8000/api/users`, requestOptions).then((response) => {
        console.log(response.statusText)
        if (response.statusText != 'OK') {
            console.log("here")
          setErrorMessage(response.data.detail)
        } else {
            console.log(response.data.access_token)
          setToken(response.data.access_token)
        }
    })
    console.log(setToken)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (password === confirmationPassword && password.length > 5) {
      submitRegistration()
    } else {
      setErrorMessage(
        "Ensure that the passwords match and greater than 5 characters"
      )
    }
  }

  return (
    <div className="registration">
        <h1>Registration</h1>
        <form onSubmit={handleSubmit}>
            <input type="text" placeholder="Enter login" id="login-reg" value={login} onChange={(e) => setLogin(e.target.value)} required />
            <input type="password" placeholder="Enter Password" id="psw-reg" value={password} onChange={(e) => setPassword(e.target.value)} required />
            <input type="password" placeholder="Repeat Password" id="psw-repeat-reg" value={confirmationPassword} onChange={(e) => setConfirmationPassword(e.target.value)} required />
            <ErrorMessage message={errorMessage} />
            <p><button className="submit" type="submit">Register</button></p>
        </form>
    </div>
  )
}

export default Register