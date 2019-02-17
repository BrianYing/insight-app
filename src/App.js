import React, { Component } from 'react';
import Insight from './components/Insight';

import './App.css';


class App extends Component {
  render() {
    return(
        <div className="form">
            <div className="box sb1">Enter Company Ticker to Search</div>
            <form action="http://localhost:5000/result" method="get">
                <fieldset>
                    <input type = "search" name="place"/>
                        <button type = "submit"> <i className = "fa fa-search" ></i>
                        </button >
                </fieldset>
            </form >
            {/*<form action="http://localhost:5000/result" method="get">*/}
                {/*Place: <input type="text" name="place" className="input"/>*/}
                {/*<input type="submit" value="Submit"/>*/}
            {/*</form>*/}
        </div>
    )
  }
}

export default App;
