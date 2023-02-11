import React from 'react'
import MoviesItemPage from '../components/MoviesItemPage'


class MoviesPages extends React.Component{
    constructor(props) {
        super(props)

    }

    render() {
        let pages = [1, this.props.last_page];
        if (this.props.current_page - 1 > 1){
            pages = [...pages, this.props.current_page - 1]
        }
        if (this.props.current_page + 1 < this.props.last_page){
            pages = [...pages, this.props.current_page + 1]
        }
        if (this.props.current_page != 1 & this.props.current_page != this.props.last_page){
            pages = [...pages, this.props.current_page]
        }

        return(
            <div class="container">
                <div class="row">
                    <div class="pages">
                        <ul>
                            {Array.from(Array(this.props.last_page + 1), (e, i) => {
                                if(pages.includes(i + 1)){
                                    return <MoviesItemPage id={i + 1} is_current_page={this.props.current_page == i + 1 ? 'yes' : 'no'} />
                                }
                            })}
                        </ul>
                    </div>
                </div>
            </div>
        )
    }
}

export default MoviesPages