import React from "react";
import "../static/css/form.css";
import HeaderComponent from "../components/header";
import axios from "axios";
import get_cookie from "../functions/get_cookie";
import {Navigate} from "react-router-dom";
import ErrorComponent from "../components/error";
import GoodComponent from "../components/good";
import ChooseInput from "../components/choose_input";


class AddProxiesForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            proxy_type: "http",
            proxies: ""
        };
        this.changeTaskData = this.changeTaskData.bind(this);
        this.chooseProxyType = this.chooseProxyType.bind(this);
        this.createProxies = this.createProxies.bind(this);
    }

    changeTaskData(event) {
        const data_name = event.target.id;
        const data_value = event.target.value;
        const new_data = {};
        new_data[data_name] = data_value;
        this.setState(new_data);
    }
    
    chooseProxyType(event) {
        const proxy_name = event.target.id;
        this.setState({
            proxy_type: proxy_name
        });
    }

    async createProxies() {
        const proxy_type = this.state.proxy_type;
        const proxies_list = this.state.proxies.split("\n");
        for (let i = 0; i < proxies_list.length; i++) {
            let proxy = proxies_list[i].split(':');
            let form = new FormData();
            form.append("proxy_model_type", proxy_type);
            form.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
            if (proxy.length === 2) {
                form.append("proxy_model_ip", proxy[0]);
                form.append("proxy_model_port", proxy[1]);
                form.append("proxy_model_username", "");
                form.append("proxy_model_password", "");
            }
            else if(proxy.length === 4) {
                form.append("proxy_model_ip", proxy[0]);
                form.append("proxy_model_port", proxy[1]);
                form.append("proxy_model_username", proxy[2]);
                form.append("proxy_model_password", proxy[3]);
            }
            const setNavigateTo = this.props.setNavigateToFunction;
            await axios({
                method: "POST",
                url: "https://api.tgpanel.com.ru/proxy/create",
                data: form
            }).then((response) => {
                if (response.data.error === "Вы не авторизованы") {
                    setNavigateTo("/login")
                }
            });
        }
        this.props.updateGoodFunction(true, "Прокси успешно добавлены")
        setTimeout(() => {
            this.props.setNavigateTo("/get_proxies");
        }, 1000)
    }

    render() {
        return (
            <div className="main-data">
                <h1 className="header">Добавить прокси</h1>
                <div className="form">
                    <div className="form-input-with-label">
                        <span>
                            Тип прокси
                        </span>
                        <ChooseInput
                            choose_buttons = {[
                                {
                                    "name": "http",
                                    "text": "HTTP"
                                },
                                {
                                    "name": "socks4",
                                    "text": "SOCKS4"
                                },
                                {
                                    "name": "socks5",
                                    "text": "SOCKS5"
                                },
                            ]}
                            chosen_type = {this.state.proxy_type}
                            chooseFunction = {this.chooseProxyType}
                        />
                    </div>
                    <div className="form-input-with-label">
                        <span>
                            Список прокси
                        </span>
                        <textarea id="proxies" placeholder={"IP:PORT" + "\n" + "IP:PORT:USERNAME:PASSWORD"} onChange={this.changeTaskData}>
                        </textarea>
                    </div>
                    <button className="button" onClick={this.createProxies}>
                        Создать аккаунты
                    </button>
                </div>
            </div>
        );
    }
}


class AddProxiesPage extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            error_status: false,
            error_text: "",
            good_status: false,
            good_text: "",
            login_check_timer: undefined,
            is_logged_in: undefined,
            navigate_to: ""
        }
        this.updateGood = this.updateGood.bind(this);
        this.updateError = this.updateError.bind(this);
        this.checkIsUserAuth = this.checkIsUserAuth.bind(this);
        this.setUserIsNotAuth = this.setUserIsNotAuth.bind(this);
        this.setNavigateTo = this.setNavigateTo.bind(this);
        this.closeWindows = this.closeWindows.bind(this);

    }

    updateGood(good_status, good_text) {
       
        this.setState({
            good_status: good_status,
            good_text: good_text,
            error_status: false,
            error_text: ""
        })
    }

    updateError(error_status, error_text) {
        
        this.setState({
            error_status: error_status,
            error_text: error_text,
            good_status: false,
            good_text: false
        })
    }


    closeWindows() {
        this.setState({
            error_status: false,
            error_text: false,
            good_status: false,
            good_text: false
        })
    }

    checkIsUserAuth() {
        const login_form = new FormData()
        login_form.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
        axios({
            method: "POST",
            url: "https://api.tgpanel.com.ru/admin/check_auth", data: login_form
        }).then((response) => {
            if (!response.data.status) {
                this.setUserIsNotAuth()
            } 
            else {
                this.setState({
                    is_logged_in: true
                })
            }
        })
    }

    setUserIsNotAuth() {
        this.setState({
            is_logged_in: false
        })
    }

    setNavigateTo(navigate_to) {
        this.setState({
            navigate_to: navigate_to
        })
    }

    componentDidMount() {
        this.checkIsUserAuth()
        const login_check_timer = setInterval(this.checkIsUserAuth, 10000)
        this.setState({
            login_check_timer: login_check_timer
        })
    }

    componentWillUnmount() {
        clearInterval(this.state.login_check_timer)
    }

    render() {
        let check_login = undefined
        let navigate_to = undefined
        if (this.state.is_logged_in !== undefined) {
            check_login = this.state.is_logged_in ?  undefined : <Navigate to="/login" replace={true} />
        }
        if (this.state.navigate_to !== "") {
            navigate_to = <Navigate to={this.state.navigate_to} replace={true} />
        }
        return (
            <div>
                {check_login}
                {navigate_to}
                <HeaderComponent />
                <ErrorComponent is_show={this.state.error_status} text={this.state.error_text} closeWindowsFunction={this.closeWindows}/>
                <GoodComponent is_show={this.state.good_status} text={this.state.good_text} closeWindowsFunction={this.closeWindows} />
                <AddProxiesForm updateGoodFunction={this.updateGood} updateErrorFunction={this.updateError}
                                setNavigateToFunction={this.setNavigateTo}/>
            </div>
        );
    }
}

export default AddProxiesPage
