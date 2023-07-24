import React from "react";
import HeaderComponent from "../components/header";
import PaginationComponent from "../components/pagination";

import EditIcon from "../static/img/edit_icon.svg";
import DeleteIcon from "../static/img/delete_icon.svg";

import "../static/css/table.css";
import axios from "axios";
import get_cookie from "../functions/get_cookie";
import {Navigate} from "react-router-dom";
import ErrorComponent from "../components/error";
import GoodComponent from "../components/good";


class GetTasksTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            tasks: [],
            count_pages: 0,
            active_page: 1
        }
        this.updateTasks = this.updateTasks.bind(this);
        this.changePage = this.changePage.bind(this);
        this.deleteTask = this.deleteTask.bind(this);
    }


    updateTasks() {
        const form = new FormData()
        form.append("page", this.state.active_page)
        form.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
        const setNavigateTo = this.props.setNavigateToFunction;
        axios({
            method: "POST",
            url: "https://api.tgpanel.com.ru/task/get_pagination",
            data: form
        }).then(
            (response) => {
                if (response.data.status) {
                    this.setState({
                        tasks: response.data.data.tasks,
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
        this.updateTasks()
    }

    async deleteTask(event) {
        const task_model_id = event.target.id.split("_")[1]
        const formData = new FormData()
        formData.append("task_model_id", task_model_id)
        formData.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
        const setNavigateTo = this.props.setNavigateToFunction;
        await axios({
            method: "POST",
            url: "https://api.tgpanel.com.ru/tasks/delete",
            data: formData
        }).then((response) => {
            if (response.data.error === "Вы не авторизованы") {
                setNavigateTo("/login")
            }
        })
        this.updateTasks()
    }

    componentDidMount() {
        this.updateTasks()
    }

    render() {
        return (
            <div>
                <table className="main-table">
                    <thead>
                        <tr>
                            <th>№</th>
                            <th>Тип задачи</th>
                            <th>Название задачи</th>
                            <th>Дата создания</th>
                            <th>Статус</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {this.state.tasks.map((task) => {
                            var status_bar_type = "status-bar-ready-red"
                            let percent = task['count_makes'] / task['required_count'] * 100
                            if (percent > 25) {
                                status_bar_type = "status-bar-ready-yellow"
                            }
                            if (percent > 50) {
                                status_bar_type = "status-bar-ready-blue"
                            }
                            if (percent > 75) {
                                status_bar_type = "status-bar-ready-green"
                            }
                            if (percent > 100) {
                                percent = 100
                            }
                            return <tr>
                                <td>{task['id']}</td>
                                <td>
                                    {task['type']}
                                </td>
                                <td>
                                    <div className="task-type">
                                        <span>{task['name']}</span>
                                        <a href={task['channel_link']}>{task['channel_link']}</a>
                                    </div>
                                </td>

                                <td>{task['start_time']}</td>
                                <td>
                                    { task['type'] !== "parse_vk" ?
                                        <div className="status">
                                            <div className="status-text">
                                            <span className="counter">
                                                {task['count_makes']} / {task['required_count']}
                                            </span>
                                                {task['type'] !== "accounts_create" ? <span>
                                                    Завершение {task['end_time']}
                                                </span> : <span>Задание активно</span>}
                                            </div>
                                            <div className="status-bar">
                                                <div className={"status-bar-ready " + status_bar_type} style={{
                                                    "width": percent + "%"
                                                }}/>
                                            </div>
                                        </div> : undefined
                                    }
                                </td>
                                <td>
                                    <button id={"task_" + task['id']} onClick={this.deleteTask}>
                                        <img id={"task_" + task['id']} src={DeleteIcon} alt="delete_icon" />
                                    </button>
                                </td>
                            </tr>
                        })}
                    </tbody>
                </table>
            </div>
        );
    }
}


class GetTasksPage extends React.Component {
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
                <GetTasksTable updateGoodFunction={this.updateGood} updateErrorFunction={this.updateError}
                                setNavigateToFunction={this.setNavigateTo} />
                <PaginationComponent updateGoodFunction={this.updateGood} updateErrorFunction={this.updateError}
                                setNavigateToFunction={this.setNavigateTo} />
            </div>
        );
    }
}

export default GetTasksPage
