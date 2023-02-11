import React from 'react'
import './css/App.css'
import Home from './pages/Home'
import Movies from './pages/Movies'
import ItemMovie from './pages/ItemMovie'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import * as ReactDomClient from 'react-dom/client'


class App extends React.Component{

    render() {
        return(
            <Router>
                <Routes>
                    <Route path="/" element={<Home/>} exact/>
                    <Route path="/movies" element={<Movies path="/movies" />} exact/>
                    <Route path="/movies/pages/:id" element={<Movies path="/movies/pages/" />} exact/>
                    <Route path="/movie/:id" element={<ItemMovie/>} />
                </Routes>
            </Router>
        )
    }
}


const app = ReactDomClient.createRoot(document.getElementById("app"))
app.render(<App />)

export default App
