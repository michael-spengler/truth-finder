import React, { Component } from 'react'

    class Account extends Component {
        render() {
        return (
            <div id="content" >
                <header class="masthead">
                    <div class="container">
                        <h2>Account</h2>
                        <small className="text-secondary">
                        <small id="account">{this.props.account}</small>
                        </small> 
                    </div>
                </header>
            </div>
        );
    }
}
    
export default Account;