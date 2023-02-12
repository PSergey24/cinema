import React, { createContext, useEffect, useState } from "react"
import axios from 'axios'

export const UserContext = createContext()

export const UserProvider = (props) => {
    const [token, setToken] = useState(localStorage.getItem("awesomeLeadsToken"))

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
                    console.log(response.data.login)
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
    <UserContext.Provider value={[token, setToken]}>
      {props.children}
    </UserContext.Provider>
  )
}