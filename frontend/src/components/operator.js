import React from "react";
import axios from "axios";
import { Form, Input, Button, Divider, Card } from "antd";

class Operator extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			currentUser: this.props.currentUser,
			bikeid: "",
		};
		this.handleChange = this.handleChange.bind(this);
	}

	handleChange(event) {
		const value = event.target.value;
		const name = event.target.id;
		this.setState({ [name]: value });
	}

	handleOperator(operation) {
		axios
			.post(`http://127.0.0.1:8000/api/oper/`, {
				bikeid: JSON.stringify(this.state.bikeid),
				operation: JSON.stringify(operation),
				uid: JSON.stringify(this.state.currentUser[0]),
			})
			.then(
				(response) => {
					if (response.data.error == "error") {
						console.log("Error: Server");
						this.displayNotification("Error: Server");
					} else {
						let rst = response.data.result;
						this.displayNotification(rst);
					}
				},
				function (err) {
					console.log("Error: Client", err);
					this.displayNotification(err);
				}
			);
	}

	displayNotification(rst) {
		let notify = document.getElementById("notification");
		if (typeof rst == "string") {
			notify.innerText = rst;
			setTimeout(() => {
				notify.innerText = "";
			}, 3500);
		} else {
			if (document.getElementById("ul001") != null) {
				notify.removeChild(document.getElementById("ul001"));
			}
			let ulNode = document.createElement("ul");
			ulNode.id = "ul001";
			notify.appendChild(ulNode);
			for (let i in rst) {
				let liNode = document.createElement("li");
				liNode.innerText = i + ": " + rst[i];
				ulNode.appendChild(liNode);
			}
		}
	}

	render() {
		const wholeStyle = {
			display: "flex",
			alignItems: "center",
			justifyContent: "flex-start",
			flexDirection: "column",
			height: "100vh",
			width: "100vw",
		};
		const flex = {
			display: "flex",
			alignItems: "center",
			justifyContent: "center",
		};
		const maintitle = {
			fontSize: "2.5em",
			display: "flex",
			alignItems: "center",
			justifyContent: "center",
			fontWeight: "bolder",
		};
		const cardStyle = {
			backgroundColor: "transparent",
			border: "2px dashed white",
			boxShadow: "10px 10px 5px #888888",
			width: "50vw",
		};
		const btnStyle = {
			backgroundColor: "rgba(0,0,0,0.7)",
			color: "white",
			fontSize: "1.4em",
			width: "15vw",
		};
		return (
			<div style={wholeStyle}>
				<h1 style={maintitle}>Operator</h1>
				{/* repair */}
				<Card style={cardStyle}>
					<Divider plain>Repair Bikes</Divider>
					<Form>
						{/* bike ID */}
						<Form.Item
							label="bike ID"
							name="bikeid"
							rules={[{ required: true, message: "Please input bikeID" }]}
						>
							<Input
								value={this.state.bikeid}
								onChange={this.handleChange.bind(this)}
							/>
						</Form.Item>
						{/* rent bike */}
						<Form.Item>
							<section style={flex}>
								<Button
									shape="round"
									size="large"
									block
									style={btnStyle}
									htmlType="button"
									onClick={(e) => this.handleOperator("repair", e)}
								>
									Report for repair
								</Button>
							</section>
						</Form.Item>
					</Form>
				</Card>
				<Card style={cardStyle}>
					{/* track bikes */}
					<Divider plain>Track Bikes</Divider>
					<Form>
						<Form.Item>
							<section style={flex}>
								<Button
									shape="round"
									htmlType="button"
									size="large"
									block
									style={btnStyle}
									onClick={(e) => this.handleOperator("track", e)}
								>
									Track Bikes
								</Button>
							</section>
						</Form.Item>
					</Form>
				</Card>
				<Card style={cardStyle}>
					{/* balance bikes */}
					<Divider plain>Balance Bikes</Divider>
					<Form>
						<Form.Item>
							<section style={flex}>
								<Button
									shape="round"
									size="large"
									block
									style={btnStyle}
									htmlType="button"
									onClick={(e) => this.handleOperator("balance", e)}
								>
									Balance Bikes
								</Button>
							</section>
						</Form.Item>
					</Form>
				</Card>
			</div>
		);
	}
}

export default Operator;
