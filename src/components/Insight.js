import React, { Component } from 'react';

import './Insight.css';

// class Insight extends Component {
//     render(props) {
//         const result = this.props.result;
//         return (
//             <div>
//                 <div className="box_title">Company</div>
//                 <div className="box_sum">Stock:</div>
//                 <div className="box_sum1">Summary:</div>
//                 <div className="box_sum2">Company News:</div>
//                 <div className="box_sum3">Call Transcript:</div>
//
//             </div>
//         );
//     }
// }

const Insight = props => (
	<div>
		<div className="box_title">Company</div>
		<div className="box_sum">Stock: </div>
		<div className="box_sum1">Summary:</div>
		<div className="box_sum2">Company News:</div>
		<div className="box_sum3">Call Transcript:</div>
	</div>
);

export default Insight;
