import React, { createContext, useEffect, useState } from "react"
import axios from 'axios'

export const UserContext = createContext()

export const UserProvider = (props) => {
    const [token, setToken] = useState(localStorage.getItem("awesomeLeadsToken"))
    const [name, setName] = useState(null)
    const [ratings, setRatings] = useState([])
    const [likes, setLikes] = useState([])

    useEffect(() => {
        const fetchUser = () => {
            if (token != 'null'){
                const requestOptions = {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: {"token": token},
                }

                axios.post(`http://0.0.0.0:8000/api/users/me`, requestOptions).then((response) => {
                    setName(response.data.login)
                    setRatings(response.data.my_ratings)
                    setLikes(response.data.my_likes)
                    if (response.statusText != 'OK') {
                        setToken('null')
                    }

                })
            }
            localStorage.setItem("awesomeLeadsToken", token)
        }
        fetchUser()
  }, [token])

  return (
    <UserContext.Provider value={[token, setToken, name, setName, ratings, likes]}>
      {props.children}
    </UserContext.Provider>
  )
}