import React from "react";

import HeaderComponent from "../components/header";

import NextIconDarkGreen from "../static/img/next_dark_green.svg";
import NextIconBlue from "../static/img/next_blue.svg";
import NextIconBrown from "../static/img/next_brown.svg";

import axios from "axios";
import "../static/css/dashboard.css";
import {Link} from "react-router-dom";

import { Navigate } from "react-router-dom";
import get_cookie from "../functions/get_cookie";
import ErrorComponent from "../components/error";
import GoodComponent from "../components/good";


class DashboardElement extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            count_accounts: 0,
            count_new_accounts: 0,
            count_banned_accounts: 0,
            count_proxies: 0,
            count_channels: 0,
            count_makes_this_day: 0,
            count_makes_all: 0,
            count_active_tasks: 0
        }
        this.updateStats = this.updateStats.bind(this);
    }

    updateStats() {
        const setNavigateTo = this.props.setNavigateToFunction;
        const form = new FormData()
        form.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
        axios({
            method: "POST",
            url: "https://api.tgpanel.com.ru/get_stats",
            data: form
        }).then((response) => {
            if (response.data.status) {
                this.setState({
                    count_accounts: response.data.data[0],
                    count_new_accounts: response.data.data[2],
                    count_banned_accounts: response.data.data[1],
                    count_proxies: response.data.data[3],
                    count_channels: response.data.data[4],
                    count_makes_this_day: response.data.data[5],
                    count_makes_all: response.data.data[6],
                    count_active_tasks: response.data.data[7]
                })
            }
            else {
                if (response.data.error !== "Вы не авторизованы") {
                    this.updateErrorFunction(true, "Не удалось получить данные")
                }
                else {
                    setNavigateTo("/login")
                }
            }
        })
    }


    componentDidMount() {
        this.updateStats()
    }


    render() {
        return (
          <div className="main-data">
              <h1 className="header">
                  Личный кабинет
              </h1>
              <div className="dashboard-row">
                  <div className="dashboard-block" style={{"width": "43%"}}>
                      <div className="dashboard-additional-block">
                          <Link to="/get_accounts" className="dashboard-data dashboard-blue-background" style={{"width": "100%"}}>
                              <span className="dashboard-data-title">Количество аккаунтов</span>
                              <span className="dashboard-data-counter">{this.state.count_accounts}</span>
                              <Link to="/add_accounts" className="dashboard-create-button">
                                  <span>Добавить аккаунты</span>
                                  <img src={NextIconBlue} alt="next-icon"/>
                              </Link>
                          </Link>
                      </div>
                      <div className="dashboard-additional-block">
                          <div className="dashboard-data dashboard-blue-border" style={{"width": "33%"}}>
                              <span className="dashboard-data-title">Новые</span>
                              <span className="dashboard-data-counter">{this.state.count_new_accounts}</span>
                          </div>
                          <div className="dashboard-data dashboard-red-border" style={{"width": "33%"}}>
                              <span className="dashboard-data-title">Забанены</span>
                              <span className="dashboard-data-counter">{this.state.count_banned_accounts}</span>
                          </div>
                      </div>
                  </div>
                  <div className="dashboard-block" style={{"width": "43%"}}>
                      <div className="dashboard-additional-block">
                          <Link to="/get_proxies" className="dashboard-data dashboard-light-gray" style={{"width": "100%"}}>
                              <span className="dashboard-data-title">Количество прокси</span>
                              <span className="dashboard-data-counter">{this.state.count_proxies}</span>
                              <Link to="/add_proxies" className="dashboard-create-button">
                                  <span>Добавить прокси</span>
                                  <img src={NextIconBrown} alt="next-icon"/>
                              </Link>
                          </Link>
                      </div>
                      <div className="dashboard-additional-block">
                          <Link to="/get_channels" className="dashboard-data dashboard-dark-gray" style={{"width": "100%"}}>
                              <span className="dashboard-data-title">Количество каналов</span>
                              <span className="dashboard-data-counter">{this.state.count_channels}</span>
                          </Link>
                      </div>
                  </div>
              </div>
              <div className="dashboard-row">
                  <div className="dashboard-block" style={{"width": "100%"}}>
                      <div className="dashboard-additional-block">
                          <div className="dashboard-data dashboard-main-color">
                              <span className="dashboard-data-title">Количество действий за сутки</span>
                              <span className="dashboard-data-counter">{this.state.count_makes_this_day}</span>
                          </div>
                          <div className="dashboard-data dashboard-main-color">
                              <span className="dashboard-data-title">Количество действий всего</span>
                              <span className="dashboard-data-counter">{this.state.count_makes_all}</span>
                          </div>
                          <Link to="/get_tasks" className="dashboard-data dashboard-dark-green">
                              <span className="dashboard-data-title">Запущенных задач</span>
                              <span className="dashboard-data-counter">{this.state.count_active_tasks}</span>
                              <Link to="/add_task" className="dashboard-create-button">
                                  <span>Новая задача</span>
                                  <img src={NextIconDarkGreen} alt="next-icon"/>
                              </Link>
                          </Link>
                      </div>
                  </div>
              </div>
          </div>
        );
    }
}

class DashboardPage extends React.Component {
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
                <DashboardElement updateGoodFunction={this.updateGood} updateErrorFunction={this.updateError}
                                setNavigateToFunction={this.setNavigateTo} />
            </div>
        );
    }
}

export default DashboardPage