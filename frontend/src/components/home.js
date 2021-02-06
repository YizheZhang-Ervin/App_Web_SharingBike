import React from 'react';
import { Menu } from 'antd';
import Customer from './customer';
import Operator from './operator';
import Manager from './manager';
import Login from './login';
import bgimg from '../static/bikebg.jpg'

class Home extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            userInterface:"login",
            currentUser: "",
            menuSelected:["login"],
        };
    }
    // 向子组件login传值
    getUser(role,userobj){
        this.setState({
            currentUser:userobj,
            userInterface:role,
            menuSelected:[role]
        });
    }
    // 改变显示的组件
    changeShow =(e)=> {
        this.setState({
            userInterface: e.key,
            menuSelected:e.key,
        })
    }

    render() {
        const wholeStyle = {
            backgroundSize:"cover",
            backgroundImage:`url(${bgimg})`,
            width:"100vw",
        }
        // change component show
        let UserInterface = null;
        let ui = this.state.userInterface;
        if(ui=="customer"){
            UserInterface = <Customer currentUser={this.state.currentUser}></Customer>
        }else if(ui=="operator"){
            UserInterface = <Operator currentUser={this.state.currentUser}></Operator>
        }else if(ui=="manager"){
            UserInterface = <Manager currentUser={this.state.currentUser}></Manager>
        }else{
            UserInterface = <Login getUser={this.getUser.bind(this)}></Login>
        }
        return (
            <div>
                {/* small screen part */}
                <div id="smallpart">
                    <h1>This is the system for PC Browser, please use laptop or larger screen device!</h1>
                </div>
                {/* normal part */}
                <section id="normalpart" style={wholeStyle}>
                    {/* menu */}
                    <Menu theme="dark" mode="horizontal" onClick={this.changeShow} selectedKeys={this.state.menuSelected}
                        onChange={this.changeShow}
                    >
                        <Menu.Item key="login">
                            Home
                        </Menu.Item>
                        <Menu.Item key="customer" disabled>
                            Customer
                        </Menu.Item>
                        <Menu.Item key="operator" disabled>
                            Operator
                        </Menu.Item>
                        <Menu.Item key="manager" disabled>
                            Manager
                        </Menu.Item>
                    </Menu>
                    {/* notification */}
                    <h1 id="notification"></h1>
                    {/* login or customer or operator or manager */}
                    {UserInterface}
                </section>
            </div>
        )
    }
}

export default Home;