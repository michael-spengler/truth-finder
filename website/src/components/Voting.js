
import React,{ useState, Component } from 'react';
import { simpleStorageAbi } from 'D:/Programmiershit/bittemach/src/abis/abis.js';
import Web3 from 'web3'

const web3 = new Web3(Web3.givenProvider)

// contract address is provided by Truffle migration
const contractAddr = '0xf58Ed5BEb28617c0D24EAa06A8B9c7a95267133D';
const SimpleContract = new web3.eth.Contract(simpleStorageAbi, contractAddr);

function Voting() {
    const [number, setNumber] = useState(0);
    const [getNumber, setGetNumber] = useState('0x00');

    const handleGet = async (e) => {
        e.preventDefault();
        const result = await SimpleContract.methods.get().call();
        setGetNumber(result);
        console.log(result);
      }

      const handleSet = async (e) => {
        e.preventDefault();    
        const accounts = await window.ethereum.enable();
        const account = accounts[0];
        const gas = await SimpleContract.methods.set(number)
                            .estimateGas();
        const result = await SimpleContract.methods.set(number).send({
          from: account,
          gas 
        })
        console.log(result);
      }



    return (
        <div id="content" >
            <header class="masthead">
                <div class="container">
                    <form onSubmit={handleSet}>
                    <label>
                        Set Number:
                        <input 
                        type="text"
                        name="name"
                        value={number}
                        onChange={ e => setNumber(e.target.value) } />
                    </label>
                    <input type="submit" value="Set Number" />
                    </form>
                    <br/>
                    <button
                    onClick={handleGet}
                    type="button" > 
                    Get Number 
                    </button>
                    { getNumber }
                    </div> 
          
          </header>
        
        </div> 
    );

    
}

export default Voting;
