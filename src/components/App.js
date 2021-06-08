import React, { Component } from 'react'
import Web3 from 'web3'
import TokenFarm from '../abis/TokenFarm.json'
import Navbar from './Navbar'
import Main from './Main'
import './App.css'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import About from "./About"
import Account from "./Account"
import Voting from "./voting"


class App extends Component {

  async componentWillMount() {
    this.loadWeb3()
    this.loadBlockchainData()
  }

  async loadBlockchainData() {
    const web3 = window.web3

    const accounts = await web3.eth.getAccounts()
    this.setState({ account: accounts[0] })

    const networkId = await web3.eth.net.getId()

    // // Load TokenFarm
    // const tokenFarmData = TokenFarm.networks[networkId]
    // if(tokenFarmData) {
    //   const tokenFarm = new web3.eth.Contract(TokenFarm.abi, tokenFarmData.address)
    //   this.setState({ tokenFarm })
    //   let stakingBalance = await tokenFarm.methods.stakingBalance(this.state.account).call()
    //   this.setState({ stakingBalance: stakingBalance.toString() })
    // } else {
    //   window.alert('TokenFarm contract not deployed to detected network.')
    // }

    // this.setState({ loading: false })
  }

  async loadWeb3() {
    if (window.ethereum) {
      window.web3 = new Web3(window.ethereum)
      await window.ethereum.enable()
    }
    else if (window.web3) {
      window.web3 = new Web3(window.web3.currentProvider)
    }
    else {
      window.alert('Non-Ethereum browser detected. You should consider trying MetaMask!')
    }
  }


 
  // stakeTokens = (amount) => {
  //   this.setState({ loading: true })
  //   this.state.daiToken.methods.approve(this.state.tokenFarm._address, amount).send({ from: this.state.account }).on('transactionHash', (hash) => {
  //     this.state.tokenFarm.methods.stakeTokens(amount).send({ from: this.state.account }).on('transactionHash', (hash) => {
  //       this.setState({ loading: false })
  //     })
  //   })
  // }

  // unstakeTokens = (amount) => {
  //   this.setState({ loading: true })
  //   this.state.tokenFarm.methods.unstakeTokens().send({ from: this.state.account }).on('transactionHash', (hash) => {
  //     this.setState({ loading: false })
  //   })
  // }

  constructor(props) {
    super(props)
    this.state = {
      account: 'Keine Account ID vorhande, bitte anmelden.',
      daiToken: {},
      dappToken: {},
      tokenFarm: {},
      daiTokenBalance: '0',
      dappTokenBalance: '0',
      stakingBalance: '0',
      loading: true
    }
  }

  render() {
    

    return (
      <Router>
      <div>
        <Navbar/>
      
        

      <Switch>
        <Route exact path="/Main">
          <Main />
        </Route>
        <Route path="/About">
          <About />
        </Route>
        <Route path="/Account">
          <Account account={this.state.account}/>
        </Route>
        <Route path="/voting">
          <Voting/>
        </Route>
      </Switch>
      </div>
    </Router>

    );
  }
}

export default App;
