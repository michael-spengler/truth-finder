import React, { Component } from 'react'

    class Account extends Component {
        render() {
        return (
            <div id="content" >
                <header class="masthead">
                    <div class="container">
                        <h2>Account Id:</h2>

                        <h2 id="account">{this.props.account}</h2>

                    </div>
                </header>
            </div>
        );
    }
}
    
export default Account;