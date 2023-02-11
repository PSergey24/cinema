import React from 'react'


class HomeRegistrationForm extends React.Component{

    render() {
        return(
            <div className="form">
                <div className="registration">
                    <h1>Registration</h1>
                    <form>
                        <input type="text" placeholder="Enter login" name="email" id="login" required />
                        <input type="password" placeholder="Enter Password" name="psw" id="psw" required />
                        <input type="password" placeholder="Repeat Password" name="psw-repeat" id="psw-repeat" required />

                        <p><button className="submit" type="button">Register</button></p>
                    </form>
                </div>
                <div className="authorization">
                    <form>
                        <h1>Authorization</h1>
                        <input type="text" placeholder="Enter login" name="login" id="login" required />
                        <input type="password" placeholder="Enter Password" name="psw" id="psw" required />

                        <p><button className="submit">Login</button></p>
                    </form>
                </div>
            </div>
        )
    }
}

export default HomeRegistrationForm