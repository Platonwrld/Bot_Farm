import React from "react";
import HeaderComponent from "../components/header";

import EditIcon from "../static/img/edit_icon.svg";
import DeleteIcon from "../static/img/delete_icon.svg";

import "../static/css/table.css";
import "../static/css/windowform.css";
import axios from "axios";
import PaginationComponent from "../components/pagination";
import get_cookie from "../functions/get_cookie";
import {Navigate} from "react-router-dom";
import ErrorComponent from "../components/error";
import GoodComponent from "../components/good";
import {Link} from "react-router-dom";


class GetChannelsTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            channels: [],
            count_pages: 0,
            active_page: 1,
            channel_link: "",
            form_window_opened: false
        }
        this.updateChannels = this.updateChannels.bind(this);
        this.changePage = this.changePage.bind(this);
        this.deleteChannel = this.deleteChannel.bind(this);
        this.editChannel = this.editChannel.bind(this);
        this.changeLink = this.changeLink.bind(this);
        this.confirmAdd = this.confirmAdd.bind(this);
        this.openCloseFormWindow = this.openCloseFormWindow.bind(this);
    }

    changeLink(event) {
        this.setState({
            channel_link: event.target.value
        })
    }

    confirmAdd() {
        const form = new FormData();
        form.append("channel_link", this.state.channel_link);
        form.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
        this.openCloseFormWindow()
        axios({
            method: "POST",
            url: "https://api.tgpanel.com.ru/channels/create",
            data: form
        }).then((response) => {
            if (response.data.status) {
                this.updateChannels();

            }
            if (response.data.error === "Вы не авторизованы") {
                this.props.setNavigateToFunction("/login")
            }
        });
    }

    openCloseFormWindow() {
        this.setState({
            form_window_opened: !this.state.form_window_opened,
            channel_link: ""
        })
    }


    updateChannels() {
        const form = new FormData()
        form.append("page", this.state.active_page)
        form.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
        const setNavigateTo = this.props.setNavigateToFunction;
        axios({
            method: "POST",
            url: "https://api.tgpanel.com.ru/channel/get_pagination",
            data: form
        }).then(
            (response) => {
                if (response.data.status) {
                    this.setState({
                        channels: response.data.data.channels,
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
        this.updateChannels()
    }

    async deleteChannel(event) {
        const channel_id = event.target.id.split("_")[1]
        const formData = new FormData()
        formData.append("channel_model_id", channel_id)
        formData.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
        const setNavigateTo = this.props.setNavigateToFunction;
        await axios({
            method: "POST",
            url: "https://api.tgpanel.com.ru/channel/delete",
            data: formData
        }).then((response) => {
            if (response.data.error === "Вы не авторизованы") {
                setNavigateTo("/login")
            }
        })
        this.updateChannels()
    }


    editChannel(event) {
        const channel_id = event.target.id.split("_")[1]
        this.props.setNavigateToFunction("/channel/" + channel_id)
    }

    componentDidMount() {
        this.updateChannels()
    }

    render() {
        return (
            <div style={{display: "flex", flexDirection: "column"}}>
                <div style={{display: this.state.form_window_opened ? "flex" : "none", flexDirection: "column"}} className="window-form">
                    <h1 className="form-title">Введите ссылку на канал</h1>
                    <input id = "channel_link" className="window-form-input"  value={this.state.channel_link}
                           onChange={this.changeLink} placeholder="https://t.me/"/>
                    <div className="button-group">
                        <button className="cancel-button" onClick={this.openCloseFormWindow}>Отмена</button>
                        <button className="main-button" onClick={this.confirmAdd}>Добавить канал</button>
                    </div>
                </div>
                <table className="main-table">
                    <thead>
                        <tr>
                            <th>№</th>
                            <th>Название</th>
                            <th>Ссылка</th>
                            <th>Количество подписчиков</th>
                            <th></th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.state.channels.map((channel) => {
                            console.log(channel)
                            return <tr key={channel.id}>
                                <td>
                                    {channel.id}
                                </td>
                                <td>
                                    {channel.channel_name}
                                </td>
                                <td>
                                    <a href={channel.channel_invite_link}>{channel.channel_invite_link}</a>
                                </td>
                                <td>
                                    {channel.count_subscribers}
                                </td>
                                <td>
                                    <button id={"channeledit_" + channel.id} onClick={this.editChannel}>
                                        <img id={"channeledit_" + channel.id} src={EditIcon} alt="edit_icon" />
                                    </button>
                                </td>
                                <td>
                                     <button id={"channel_" + channel.id} onClick={this.deleteChannel}>
                                        <img id={"channel_" + channel.id} src={DeleteIcon} alt="delete_icon" />
                                    </button>
                                </td>
                            </tr>
                        })}
                    </tbody>
                </table>
                <button className="table_button" onClick={this.openCloseFormWindow}>+ Добавить канал</button>
                <PaginationComponent count_pages={this.state.count_pages} active_page = {this.state.active_page} changePageFunction = {this.changePage}/>
            </div>
        );
    }
}


class GetChannelsPage extends React.Component {
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
                <GetChannelsTable updateGoodFunction={this.updateGood} updateErrorFunction={this.updateError}
                                setNavigateToFunction={this.setNavigateTo} />
            </div>
        );
    }
}

export default GetChannelsPage
