import React, { Component } from 'react';
import './components/Insight.css';

import './App.css';


class App extends Component {
    state = {
        searchHidden: false,
        resultHidden: true,
        query: "",
        result: {
            "stock_price": {},
            "stock_trend": {},
            "summary": {},
            "news": {},
            "trans": {
                "time": {},
                "max_speaker": {},
                "participants": {}
            }
        }
    };

    handleClick = async () => {
        const SERVER_URL = "http://localhost:5000/result?place=" + this.state.query;

        await fetch(SERVER_URL, {
            mode: "cors"
        })
            .then(res => res.json())
            .then(res => {
                console.log("response", res);
                this.setState({result: res, searchHidden: true, resultHidden: false})
            });
    };

    handleChange = (event) => {
        console.log("HandleChange: ", event.target.value);
        this.setState({query: event.target.value});
    };

    render() {
        return(
            <div>
                <div hidden={this.state.searchHidden} className="form">
                    <div className="box sb1">Enter Company Ticker to Search</div>
                    {/*<form onSubmit={this.handleClick.bind(this)}>*/}
                        <fieldset>
                            <input type = "search" name="place" value={this.state.query} onChange={this.handleChange}/>
                            <button type = "submit" onClick={this.handleClick.bind(this)}>
                                <i className = "fa fa-search" ></i>
                            </button>
                        </fieldset>
                    {/*</form >*/}
                </div>

                <div hidden={this.state.resultHidden}>
                    {/*<Insight result={this.state.result}></Insight>*/}
		            <div className="box_title">Company: {this.state.query}</div>
		            <div className="box_sum">
                        <table>
                            <thead>
                                <tr>
                                    <th>STOCK</th>
                                    <th></th>
                                 </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Stock Price</td>
                                    <td>{this.state.result.stock_price["price"]}</td>
                                </tr>
                                <tr>
                                    <td>Stock Trend</td>
                                    <td>{this.state.result.stock_trend["trend"]}</td>
                                </tr>
                            </tbody>
                        </table>
		            </div>

		            <div className="box_sum1">
                        <table>
                            <thead>
                                <tr>
                                    <th>SUMMARY</th>
                                    <th></th>
                                 </tr>
                            </thead>
                            <tbody>
                                {
                                    Object.keys(this.state.result.summary).map((title) => {
                                        let sums = this.state.result.summary;
                                        return (<tr>
                                                    <td>{title}</td>
                                                    <td>{sums[title]}</td>
                                                </tr>)
                                    })
                                }
                            </tbody>
                        </table>
                    </div>

		            <div className="box_sum2">
		                <table>
                            <thead>
                                <tr>
                                    <th>COMPANY NEWS</th>
                                    <th></th>
                                 </tr>
                            </thead>
                            <tbody>
                                {
                                    Object.keys(this.state.result.news).map((title) => {
                                        let urls = this.state.result.news;
                                        return (<tr>
                                                    <a href={urls[title]}>
                                                        <td>{title}</td>
                                                    </a>
                                                </tr>)
                                    })
                                }
                            </tbody>
                        </table>
		            </div>

		            <div className="box_sum3">
                        <table>
                            <thead>
                                <tr>
                                    <th>CALL TRANSCRIPT</th>
                                    <th></th>
                                 </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>Call Time</td>
                                    <td>{this.state.result.trans.time["time"]}</td>
                                </tr>
                                <tr>
                                    <td>Longest Speaker</td>
                                    <td>{this.state.result.trans.max_speaker["max_speaker"]}</td>
                                </tr>
                                <tr>
                                    <td>Participants</td>
                                    {
                                        Object.keys(this.state.result.trans.participants).map((i) => {
                                            let people = this.state.result.trans.participants;
                                            return (<tr><td>{people[i]}</td></tr>)
                                    })
                                }
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        )
    }
}

export default App;
