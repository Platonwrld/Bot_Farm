import React from "react";
import HeaderComponent from "../components/header";

import DeleteIcon from "../static/img/delete_icon.svg";

import "../static/css/table.css";
import axios from "axios";
import PaginationComponent from "../components/pagination";
import get_cookie from "../functions/get_cookie";
import {Navigate} from "react-router-dom";
import ErrorComponent from "../components/error";
import GoodComponent from "../components/good";


class GetAccountsTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            accounts: [],
            count_pages: 0,
            active_page: 1
        }
        this.updateAccounts = this.updateAccounts.bind(this);
        this.changePage = this.changePage.bind(this);
        this.deleteAccount = this.deleteAccount.bind(this);
    }

    updateAccounts() {
        const setNavigateTo = this.props.setNavigateToFunction;
        const form = new FormData()
        form.append("page", this.state.active_page)
        form.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
        axios({
            method: "POST",
            url: "https://api.tgpanel.com.ru/tg_client/get_pagination",
            data: form
        }).then(
            (response) => {
                if (response.data.status) {
                    this.setState({
                        accounts: response.data.data.tg_clients,
                        count_pages: response.data.data.count_pages
                    })
                }
                if (response.data.error === "Вы не авторизованы") {
                    setNavigateTo("/login")
                }
            }
        )
    }

    async changePage(event) {
        const new_page = event.target.id
        await this.setState({
            active_page: new_page
        })
        this.updateAccounts()
    }

    async deleteAccount(event) {
        const setNavigateTo = this.props.setNavigateToFunction;
        const channel_id = event.target.id.split("_")[1]
        const formData = new FormData()
        formData.append("tg_client_model_id", channel_id)
        formData.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
        await axios({
            method: "POST",
            url: "https://api.tgpanel.com.ru/tg_client/delete",
            data: formData
        }).then((response) => {
            if (response.data.error === "Вы не авторизованы") {
                setNavigateTo("/login")
            }
        })
        this.updateAccounts()
    }

    componentDidMount() {
        this.updateAccounts()
    }

    render() {
        return (
            <div>
                <table className="main-table">
                    <thead>
                        <tr>
                            <th>№</th>
                            <th>Номер аккаунта</th>
                            <th>Статус</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                    {this.state.accounts.map((account) => {
                        var work_status = "Работает"
                        var work_class = "green-text"
                        if (account.is_spam) {
                            work_status = "Спам блок"
                            work_class = "yeloow-text"
                        }
                        else if (account.is_ban) {
                            work_status = "Полная блокировка"
                            work_class = "red-text"
                        }
                        return <tr>
                            <td>
                                {account['id']}
                            </td>
                            <td>
                                {account['phone_number']}
                            </td>
                            <td className={work_class}>
                                {work_status}
                            </td>
                            <td>
                                <button id={"account_" + account['id']} onClick={this.deleteAccount}>
                                    <img id={"account_" + account['id']} src={DeleteIcon} alt="delete_icon" />
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


class GetAccountsPage extends React.Component {
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
                <GetAccountsTable updateGoodFunction={this.updateGood} updateErrorFunction={this.updateError}
                                setNavigateToFunction={this.setNavigateTo} />
            </div>
        );
    }
}

export default GetAccountsPage
