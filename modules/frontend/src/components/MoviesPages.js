import React from 'react'


const MoviesPages = (props) => {

    return(
        <div class="container">
            <div class="row">
                <div class="pages">
                    <ul>
                        <li><span>1</span></li>
                        <li><a href="/movies">1</a></li>
                        <li><a href="/movies/pages/1">1</a></li>
                        <li><a href="/movies/pages/2">2</a></li>
                    </ul>
                </div>
            </div>
        </div>
    )

}

export default MoviesPages