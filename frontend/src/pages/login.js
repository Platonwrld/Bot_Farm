import React from "react";
import FormLogo from "../static/img/form-logo.svg"


import HeaderComponent from "../components/header";

import "../static/css/login.css";
import axios from "axios";
import get_cookie from "../functions/get_cookie";
import setCookie from "../functions/set_cookie";
import {Navigate} from "react-router-dom";
import ErrorComponent from "../components/error";
import GoodComponent from "../components/good";


class LoginForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: "",
            password: ""
        }
        this.changeValue = this.changeValue.bind(this);
        this.sendForm = this.sendForm.bind(this);
    }

    sendForm() {
        const loginForm = new FormData()
        loginForm.append("username", this.state.username)
        loginForm.append("password", this.state.password)
        axios({
            method: "POST",
            url: "https://api.tgpanel.com.ru/admin/auth",
            data: loginForm
        }).then(
            (response) => {
                if (response.data.status) {
                    setCookie("session_hash", response.data.data, 1)
                    this.props.setNavigateToFunction("/dashboard")
                }
                else {
                    this.props.updateErrorFunction(
                        true,
                        "Введен не верный логин или пароль"
                    )
                }
            }
        )
    }

    changeValue(event) {
        var elementName = event.target.id
        var elementValue = event.target.value
        const newState = {}
        newState[elementName] = elementValue
        this.setState(newState)
    }



    render() {
        return (
            <div className="form">
                <h1 className="header">Личный кабинет</h1>
                <input id="username" type="text" className="input" placeholder="Логин" onChange={this.changeValue} />
                <input id="password" type="password" className="input" placeholder="Пароль" onChange={this.changeValue} />
                <button className="button" onClick={this.sendForm}>Войти</button>
            </div>
        );
    }
}


class LoginPageData extends React.Component {
    constructor(props) {
        super(props);
    }


    render() {
        return (
            <div className="main-form">
                <LoginForm updateGoodFunction={this.props.updateGoodFunction} updateErrorFunction={this.props.updateErrorFunction}
                                setNavigateToFunction={this.props.setNavigateToFunction}/>
                <div className="form-logo">
                    <img src={FormLogo} alt="FormLogo" />
                </div>
            </div>
        );
    }
}


class LoginPage extends React.Component {
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

    render () {
        let check_login = undefined
        let navigate_to = undefined
        if (this.state.is_logged_in !== undefined) {
            check_login = this.state.is_logged_in ? <Navigate to="/" replace={true} /> : undefined
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
                <LoginPageData updateGoodFunction={this.updateGood} updateErrorFunction={this.updateError}
                                setNavigateToFunction={this.setNavigateTo} />
            </div>
        );
    }
}

export default LoginPage