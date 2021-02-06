import React from "react";
import axios from "axios";
import { Form, Button, Divider, Card } from "antd";
import * as echarts from "echarts";
import "echarts-gl";

class Manager extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			currentUser: this.props.currentUser,
			data: null,
		};
	}

	componentDidMount() {}

	handleManager(operation) {
		axios
			.post(`http://127.0.0.1:8000/api/mgt/`, {
				operation: JSON.stringify(operation),
				uid: JSON.stringify(this.state.currentUser[0]),
			})
			.then(
				(response) => {
					if (response.data.error == "error") {
						console.log("Error: Server");
						this.displayNotification("Error: Server");
					} else {
						if (operation == "report") {
							let data = response.data.result;
							this.setState({ data: data });
							this.plot();
						} else {
							let rst = response.data.result;
							this.displayNotification(rst);
						}
					}
				},
				function (err) {
					console.log("Error: Client", err);
					this.displayNotification(err);
				}
			);
	}

	getOption = () => {
		let option = {
			grid3D: {},
			xAxis3D: { type: "category", name: "Location" },
			yAxis3D: { name: "Time" },
			zAxis3D: { name: "Bike Quantity" },
			dataset: {
				source: this.state.data,
			},
			series: [
				{
					type: "scatter3D",
					symbolSize: 3,
					encode: {
						x: "location",
						y: "time",
						z: "bikeNum",
					},
				},
			],
		};
		return option;
	};

	plot() {
		var chartDom = document.getElementById("echart");
		var myChart = echarts.init(chartDom);
		myChart.setOption(this.getOption());
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

		const chartStyle = {
			width: "100vw",
			height: "50vh",
		};
		const maintitle = {
			fontSize: "2.5em",
			display: "flex",
			alignItems: "center",
			justifyContent: "center",
			fontWeight: "bolder",
		};
		const cardStyle = {
			backgroundColor: "rgba(255,255,255,0.5)",
			border: "2px dashed white",
			boxShadow: "10px 10px 5px #888888",
			width: "50vw",
			display: "flex",
			alignItems: "center",
			justifyContent: "center",
		};
		const btnStyle = {
			backgroundColor: "rgba(0,0,0,0.7)",
			color: "white",
			fontSize: "1.4em",
			width: "15vw",
		};
		return (
			<div style={wholeStyle}>
				<h1 style={maintitle}>Manager</h1>
				{/* Data Report */}
				<Card style={cardStyle}>
					<Divider plain>Data Report</Divider>
					<Form>
						<Form.Item>
							<section style={flex}>
								<Button
									shape="round"
									size="large"
									block
									style={btnStyle}
									htmlType="button"
									onClick={(e) => this.handleManager("report", e)}
								>
									Generate Report
								</Button>
							</section>
						</Form.Item>
					</Form>
				</Card>
				<Card style={cardStyle}>
					<div id="echart" style={chartStyle}></div>
				</Card>
			</div>
		);
	}
}

export default Manager;
