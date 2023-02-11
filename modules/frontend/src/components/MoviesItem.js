import React from 'react'

class MoviesItem extends React.Component{

    render() {
        return(
            <div className="col-md-4 col-lg-4">
                <figure className="fig">
                    <img src={this.props.link} />
                    <figcaption><a href={"/movie/" + this.props.id}>{this.props.name}</a></figcaption>
                </figure>
            </div>
        )
    }
}

export default MoviesItem