import React from "react";
import axios from "axios";
import HeaderComponent from "../components/header";

import PaginationComponent from "../components/pagination";

import EditIcon from "../static/img/edit_icon.svg";
import DeleteIcon from "../static/img/delete_icon.svg";

import "../static/css/table.css";
import {upload} from "@testing-library/user-event/dist/upload";
import get_cookie from "../functions/get_cookie";
import {Navigate} from "react-router-dom";
import ErrorComponent from "../components/error";
import GoodComponent from "../components/good";


class GetProxiesTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            proxies: [],
            count_pages: 0,
            active_page: 1
        }
        this.updateProxies = this.updateProxies.bind(this);
        this.changePage = this.changePage.bind(this);
        this.deleteProxy = this.deleteProxy.bind(this);
    }

    updateProxies() {
        const form = new FormData()
        form.append("page", this.state.active_page)
        form.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
        const setNavigateTo = this.props.setNavigateToFunction;
        axios({
            method: "POST",
            url: "https://api.tgpanel.com.ru/proxy/get_pagination",
            data: form
        }).then((response) => {
            if (response.data.status) {
                this.setState({
                    proxies: response.data.data.proxies,
                    count_pages: response.data.data.count_pages
                })
            }
            if (response.data.error === "Вы не авторизованы") {
                setNavigateTo("/login")
            }
        })
    }

    async changePage(event) {
        const new_page = event.target.id
        await this.setState({
            active_page: new_page
        })
        this.updateProxies()
    }

    async deleteProxy(event) {
        const proxy_id = event.target.id.split("_")[1]
        const formData = new FormData()
        formData.append("proxy_model_id", proxy_id)
        formData.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
        const setNavigateTo = this.props.setNavigateToFunction;
        await axios({
            method: "POST",
            url: "https://api.tgpanel.com.ru/proxy/delete",
            data: formData
        }).then((response) => {
            if (response.data.error === "Вы не авторизованы") {
                setNavigateTo("/login")
            }
        })
        this.updateProxies()
    }

    componentDidMount() {
        this.updateProxies()
    }

    render() {
        return (
            <div>
                <table className="main-table">
                    <thead>
                        <tr>
                            <th>№</th>
                            <th>Type</th>
                            <th>IP</th>
                            <th>PORT</th>
                            <th>Username</th>
                            <th>Password</th>
                            <th>Количество аккаунтов</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.state.proxies.map((proxy) => {
                            return <tr key={proxy.id}>
                                <td>{proxy.id}</td>
                                <td>{proxy.type}</td>
                                <td>{proxy.ip}</td>
                                <td>{proxy.port}</td>
                                <td>{proxy.username}</td>
                                <td>{proxy.password}</td>
                                <td>{proxy.count_accounts}</td>
                                <td>
                                    <button id={"proxy_" + proxy.id} onClick={this.deleteProxy}>
                                        <img id={"proxy_" + proxy.id} src={DeleteIcon} alt="delete_icon" />
                                    </button>
                                </td>
                            </tr>
                        })}
                    </tbody>
                </table>
                <PaginationComponent count_pages={this.state.count_pages} active_page = {this.state.active_page} changePageFunction = {this.changePage}/>
            </div>
        );
    }
}


class GetProxiesPage extends React.Component {
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
                <GetProxiesTable updateGoodFunction={this.updateGood} updateErrorFunction={this.updateError}
                                setNavigateToFunction={this.setNavigateTo} />
            </div>
        );
    }
}

export default GetProxiesPage
