import React, { Component } from 'react'
import './css/Montserrat.css'
import './css/Roboto.css'
import './css/nav.css'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";






class Navbar extends Component {
  src="https://unpkg.com/react@16/umd/react.production.min.js"
  src="https://unpkg.com/react-dom@16/umd/react-dom.production.min.js"
  src="https://unpkg.com/babel-standalone@6.15.0/babel.min.js"

  render() {
    return (
      <nav class="navbar navbar-expand-lg navbar-dark fixed-top" id="mainNav">
            <div class="container">
            <Link class="navbar-brand" to="/Main"><img src={require("./assets/img/TruthFinder.png")} alt="Truth Finder" /></Link>
                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
                    Menu
                    <i class="fas fa-bars ms-1"></i>
                </button>
                <div class="collapse navbar-collapse" id="navbarResponsive">
                    <ul class="navbar-nav text-uppercase ms-auto py-4 py-lg-0">
                        <li class="nav-item"><a class="nav-link" href="{{ url_for('view_archive') }}">Services</a></li>
                        <li class="nav-item"><a class="nav-link" href="#portfolio">Portfolio</a></li>
                        <li class="nav-item"><a class="nav-link"><Link to="/About">About</Link></a></li>
                        <li class="nav-item"><a class="nav-link" href="#team">Team</a></li>
                        <li class="nav-item"><a class="nav-link"><Link to="/Account">Account</Link></a></li>
                        <li class="nav-item"><a class="nav-link" href="#contact">Contact</a></li>
                        
                        


                      
                    </ul>
                </div>
                <small className="text-secondary">
                  <small id="account">{this.props.account}</small>
                </small>
            </div>
        </nav>
    );
  }
}

export default Navbar;
