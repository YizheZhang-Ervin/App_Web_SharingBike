import React from "react";
import axios from "axios";
import { Form, Input, Button, Select, Card, Divider } from "antd";

const { Option } = Select;

class Login extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			// 向父组件home传值
			getUser: "",
			username: "",
			password: "",
			userclass: "",
		};
	}

	handleChange(event) {
		const value = event.target.value;
		const name = event.target.id;
		this.setState({ [name]: value });
	}

	loginRegister(operation, e) {
		axios
			.post(`http://127.0.0.1:8000/api/verify/`, {
				name: JSON.stringify(this.state.username),
				pwd: JSON.stringify(this.state.password),
				cls: JSON.stringify(this.state.userclass),
				operation: JSON.stringify(operation),
			})
			.then(
				(response) => {
					if (response.data.error == "error") {
						console.log("Error: Server");
						let rst = response.data.reason;
						this.displayNotification(rst);
					} else {
						// currentUser is [ID,USERCLASS]
						let currentUser = response.data.result;
						let role = currentUser[1];
						// 传给父组件
						this.props.getUser(role, currentUser);
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
			justifyContent: "center",
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
			fontSize: "3.5em",
			display: "flex",
			alignItems: "center",
			justifyContent: "center",
			fontWeight: "bolder",
		};
		const maintitle2 = {
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
		};
		const btnStyle = {
			backgroundColor: "rgba(0,0,0,0.7)",
			color: "white",
			fontSize: "1.4em",
		};
		const lineStyle = {
			color: "white",
			border: "1px white solid",
		};
		return (
			<div style={wholeStyle}>
				<h1 style={maintitle}>EZ Sharing Bike System</h1>
				<Card style={cardStyle}>
					<h1 style={maintitle2}>Login / Register</h1>
					<Form>
						{/* 用户名 */}
						<Form.Item
							label="Username"
							name="username"
							rules={[
								{ required: true, message: "Please input your username!" },
							]}
						>
							<Input
								value={this.state.username}
								onChange={this.handleChange.bind(this)}
							/>
						</Form.Item>
						{/* 密码 */}
						<Form.Item
							label="Password"
							name="password"
							rules={[
								{ required: true, message: "Please input your password!" },
							]}
						>
							<Input.Password
								value={this.state.password}
								onChange={this.handleChange.bind(this)}
							/>
						</Form.Item>
						{/* 用户类型 */}
						<Form.Item
							name="userclass"
							label="UserClass"
							rules={[{ required: true }]}
						>
							<Select
								placeholder="Select a option and change input text above"
								allowClear
								onChange={(value) => {
									this.setState({ userclass: value });
								}}
							>
								<Option value="customer">customer</Option>
								<Option value="operator">operator</Option>
								<Option value="manager">manager</Option>
							</Select>
						</Form.Item>
						{/* 登录/注册 */}
						<Form.Item>
							<section style={flex}>
								<Button
									shape="round"
									size="large"
									block
									style={btnStyle}
									htmlType="button"
									onClick={(e) => this.loginRegister("login", e)}
								>
									Login
								</Button>
								<Button
									shape="round"
									size="large"
									block
									style={btnStyle}
									htmlType="button"
									onClick={(e) => this.loginRegister("register", e)}
								>
									Register
								</Button>
							</section>
							<Divider style={lineStyle}></Divider>
							<Button
								shape="round"
								size="large"
								block
								style={btnStyle}
								htmlType="button"
							>
								<a href="/admin">Backend Login</a>
							</Button>
						</Form.Item>
					</Form>
				</Card>
			</div>
		);
	}
}

export default Login;
