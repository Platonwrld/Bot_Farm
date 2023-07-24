import React from "react";

import axios from "axios";
import "../static/css/form.css";
import HeaderComponent from "../components/header";

import ErrorComponent from "../components/error";
import GoodComponent from "../components/good";

import { Navigate } from "react-router-dom";


import get_cookie from "../functions/get_cookie";


class AddAccountsForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            task_name: "",
            sms_activate_api_key: "",
            count_accounts: 0
        }
        this.changeTaskData = this.changeTaskData.bind(this);
        this.createAccountTask = this.createAccountTask.bind(this);
        this.setSmsActivate = this.setSmsActivate.bind(this);
    }

    changeTaskData(event) {
        const data_name = event.target.id;
        const data_value = event.target.value;
        const new_data = {};
        new_data[data_name] = data_value;
        this.setState(new_data);
    }

    createAccountTask() {
        const taskForm = new FormData();
        taskForm.append("task_model_name", this.state.task_name);
        taskForm.append("task_model_type", "accounts_create");
        taskForm.append("task_model_required_count", parseInt(this.state.count_accounts));
        taskForm.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
        const setNavigateTo = this.props.setNavigateToFunction;
        const updateGoodFunction = this.props.updateGoodFunction;
        if (this.state.task_name !== "" && this.state.sms_activate_api_key !== "" && parseInt(this.state.count_accounts) > 0) {
            const sms_activate_api_key = this.state.sms_activate_api_key;
            axios({
                method: "POST",
                url: "https://api.tgpanel.com.ru/task/create",
                data: taskForm
            }).then(async (response) => {
                if (response.data.status) {
                    var startTime = new Date();
                    var date = startTime.getFullYear()+'-'+(startTime.getMonth()+1)+'-'+startTime.getDate();
                    var time = startTime.getHours()+':'+startTime.getMinutes()+':'+startTime.getSeconds();
                    startTime = date + " " + time
                    const startTimeForm = new FormData()
                    startTimeForm.append("task_argument_model_name", "start_t");
                    startTimeForm.append("task_argument_model_value", startTime);
                    startTimeForm.append("task_argument_model_task_id", response.data.data);
                    startTimeForm.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
                    await axios({
                        method: "POST",
                        url: "https://api.tgpanel.com.ru/task_argument/create",
                        data: startTimeForm
                    })
                    const taskArgumentForm = new FormData();
                    taskArgumentForm.append("task_argument_model_name", "sms_activate_api_key");
                    taskArgumentForm.append("task_argument_model_value", sms_activate_api_key);
                    taskArgumentForm.append("task_argument_model_task_id", response.data.data);
                    taskArgumentForm.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
                    await axios({
                        method: "POST",
                        url: "https://api.tgpanel.com.ru/task_argument/create",
                        data: taskArgumentForm
                    }).then((response) => {
                        if (response.data.status) {
                            updateGoodFunction(true, "Задача на создание аккаунтов успешно создана ожидайте выполнения")
                            setTimeout(() => {
                              setNavigateTo("/get_tasks");
                            }, 1000)
                        }
                        else if (response.data.error === "Вы не авторизованы") {
                            setNavigateTo("/login")
                        }
                    });
                }
                else {
                    if (response.data.error !== "Вы не авторизованы") {
                        this.updateErrorFunction(true, "Не удалось создать задачу на создание аккаунтов")
                    }
                    else {
                        setNavigateTo("/login")
                    }
                }
            });
        }
        else {
            this.props.updateErrorFunction(true, "Заполнены не все данные")
        }
    }

    setSmsActivate(api_key) {
        this.setState({
                    sms_activate_api_key: api_key
                })
    }


    componentDidMount() {
        const setSmsActivate = this.setSmsActivate;
        const form = new FormData()
        form.append("admin_login_session_model_session_hash",  get_cookie("session_hash"))
        const setNavigateTo = this.props.setNavigateToFunction;
        axios({
            method: "POST",
            url: "https://api.tgpanel.com.ru/task/get_current_sms_active",
            data: form
        }).then((response) => {
            console.log(response.data)
            if (response.data.status === true) {
                setSmsActivate(response.data.data)
            }
            else {
                setNavigateTo("/login")
            }
        })
    }

    render() {
        return (
            <div className="main-data">
                <h1 className="header">Добавить аккаунты</h1>
                <div className="form">
                    <div className="form-input-with-label">
                        <span>
                            Название задачи
                        </span>
                        <input id="task_name" type="text" onChange={this.changeTaskData}/>
                    </div>
                    <div className="form-input-with-label">
                        <span>
                            Sms Activate API
                        </span>
                        <input id="sms_activate_api_key" type="text" value={this.state.sms_activate_api_key} onChange={this.changeTaskData}/>
                    </div>
                    <div className="form-input-with-label">
                        <span>
                            Количество аккаунтов
                        </span>
                        <input id="count_accounts" type="number" min="1" onChange={this.changeTaskData}/>
                    </div>
                    <button className="button" onClick={this.createAccountTask}>
                        Создать аккаунты
                    </button>
                </div>
            </div>
        );
    }
}


class AddAccountsPage extends React.Component {
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
                <AddAccountsForm updateGoodFunction={this.updateGood} updateErrorFunction={this.updateError}
                                setNavigateToFunction={this.setNavigateTo}/>
            </div>
        );
    }
}


export default AddAccountsPage