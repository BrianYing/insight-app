import React, { Component } from 'react';
import Insight from './components/Insight';

import './App.css';


class App extends Component {
    // construtor() {
    //     this.state = {
    //         searchHidden: false,
    //         resultHidden: true,
    //         query: "",
    //         result: {}
    //     };
    //     this.handleClick = this.handleClick.bind(this);
    // }
    state = {
        searchHidden: false,
        resultHidden: true,
        query: "",
        result: undefined
    };

    // handleClick = async () => {
    //     const api_call = await fetch(`result?place=${this.state.query}`);
    //     const data = await api_call.json();
    //
    //     this.setState({result: data});
    //     this.setState({searchHidden: true});
    //     this.setState({resultHidden: false});
    // };

    handleClick = () => {
        const SERVER_URL = "result?place=" + this.state.query;

        fetch(SERVER_URL).then(res => res.json()).then(res => this.setState({result: res}));
        this.setState({searchHidden: true});
        this.setState({resultHidden: false});
        // await fetch({
        //     url: SERVER_URL,
        //     method: "GET"
        // }).then(res => res.json()).then(res => this.setState({result: res}));
    };

    render() {
        return(
            <div>
                <div hidden={this.state.searchHidden} className="form">
                    <div className="box sb1">Enter Company Ticker to Search</div>
                    <form onSubmit={this.handleClick}>
                        <fieldset>
                            <input type = "search" name="place"/>
                            <button type = "submit"> <i className = "fa fa-search" ></i>
                            </button >
                        </fieldset>
                    </form >
                </div>

                <div hidden={this.state.resultHidden}>
                    {/*<Insight result={this.state.result}></Insight>*/}
		            <div className="box_title" content={this.state.query}>Company</div>
		            <div className="box_sum" content={this.state.result}>Stock: </div>
		            <div className="box_sum1">Summary:</div>
		            <div className="box_sum2">Company News:</div>
		            <div className="box_sum3">Call Transcript:</div>
                </div>
            </div>
        )
    }
}

export default App;
