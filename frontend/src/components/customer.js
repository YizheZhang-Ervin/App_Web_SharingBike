import React from "react";
import axios from "axios";
import { Form, Input, Button, Select, Divider, Card } from "antd";
const { Option } = Select;

class Customer extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			currentUser: this.props.currentUser,
			bikeid: "",
			loc: "",
			locChoice: "",
		};
	}
	componentDidMount() {
		this.getSelections("locations");
	}

	getSelections(operation) {
		axios
			.post(`http://127.0.0.1:8000/api/select/`, {
				operation: JSON.stringify(operation),
				uid: JSON.stringify(this.state.currentUser[0]),
			})
			.then(
				(response) => {
					if (response.data.error == "error") {
						console.log("Error: Server");
						document.getElementById("notification").innerHTML = "Error: Server";
					} else {
						if (operation == "locations") {
							let rst = response.data.result;
							let lis = [];
							for (let i = 0; i < rst.length; i++) {
								lis.push(<Option value={rst[i]}>{rst[i]}</Option>);
							}
							this.setState({ locChoice: lis });
						}
					}
				},
				function (err) {
					console.log("Error: Client", err);
					document.getElementById("notification").innerHTML = err;
				}
			);
	}

	handleChange(event) {
		const value = event.target.value;
		const name = event.target.id;
		this.setState({ [name]: value });
	}

	handleCustomer(operation, e) {
		axios
			.post(`http://127.0.0.1:8000/api/cust/`, {
				bikeid: JSON.stringify(this.state.bikeid),
				loc: JSON.stringify(this.state.loc),
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
				<h1 style={maintitle}>Customer</h1>
				{/* rent bike */}
				<Card style={cardStyle}>
					<Divider plain>Rent</Divider>
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
									onClick={(e) => this.handleCustomer("rent", e)}
								>
									Rent
								</Button>
							</section>
						</Form.Item>
					</Form>
				</Card>
				{/* return bike */}
				<Card style={cardStyle}>
					<Divider plain>Return</Divider>
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
						{/* bike location */}
						<Form.Item name="loc" label="loc" rules={[{ required: true }]}>
							<Select
								placeholder="Select a option and change input text above"
								allowClear
								onChange={(value) => {
									this.setState({ loc: value });
								}}
								id="selectLocation"
							>
								{this.state.locChoice}
							</Select>
						</Form.Item>
						{/* return bike */}
						<Form.Item>
							<section style={flex}>
								<Button
									shape="round"
									size="large"
									block
									style={btnStyle}
									htmlType="button"
									onClick={(e) => this.handleCustomer("back", e)}
								>
									Rent
								</Button>
							</section>
						</Form.Item>
					</Form>
				</Card>
				{/* report for repair */}
				<Card style={cardStyle}>
					<Divider plain>Report for Repair</Divider>
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
									onClick={(e) => this.handleCustomer("report", e)}
								>
									Report for repair
								</Button>
							</section>
						</Form.Item>
					</Form>
				</Card>
			</div>
		);
	}
}

export default Customer;
