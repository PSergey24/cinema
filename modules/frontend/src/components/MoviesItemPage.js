import React from 'react'


class MoviesItemPage extends React.Component{
    constructor(props) {
        super(props)

    }


    render() {
        let content;
        if (this.props.is_current_page == "yes") {
            content = <span>{this.props.id}</span>
        } else {
            content = <a href={"/movies/pages/" + this.props.id}>{this.props.id}</a>
        }

        return(
            <li>
                {content}
            </li>
        )
    }
}

export default MoviesItemPage