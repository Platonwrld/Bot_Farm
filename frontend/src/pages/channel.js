import React from "react";

import axios from "axios";
import "../static/css/form.css";
import HeaderComponent from "../components/header";

import ErrorComponent from "../components/error";
import GoodComponent from "../components/good";

import { Navigate, useParams } from "react-router-dom";


import get_cookie from "../functions/get_cookie";
import Emoje1 from "../static/img/emojes/emoje 1.png";
import Emoje2 from "../static/img/emojes/emoje 2.png";
import Emoje3 from "../static/img/emojes/emoje 3.png";
import Emoje4 from "../static/img/emojes/emoje 4.png";
import Emoje5 from "../static/img/emojes/emoje 5.png";
import Emoje6 from "../static/img/emojes/emoje 6.png";
import Emoje7 from "../static/img/emojes/emoje 7.png";
import Emoje8 from "../static/img/emojes/emoje 8.png";
import Emoje9 from "../static/img/emojes/emoje 9.png";
import Emoje10 from "../static/img/emojes/emoje 10.png";
import Emoje11 from "../static/img/emojes/emoje 11.png";
import Emoje12 from "../static/img/emojes/emoje 12.png";
import Emoje13 from "../static/img/emojes/emoje 13.png";
import Emoje14 from "../static/img/emojes/emoje 14.png";
import Emoje15 from "../static/img/emojes/emoje 15.png";
import Emoje16 from "../static/img/emojes/emoje 16.png";
import Emoje17 from "../static/img/emojes/emoje 17.png";

import ChooseInput from "../components/choose_input";
class ChannelEditForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            channel_name: "",
            view_percent_from: 0,
            view_percent_to: 0,
            channel_reactions: [],
            emoji_now: []
        }
        this.loadChannelData = this.loadChannelData.bind(this);
        this.changeValue = this.changeValue.bind(this);
        this.updateChannelSettings = this.updateChannelSettings.bind(this);
        this.chooseEmoji = this.chooseEmoji.bind(this);
        this.onChangeEmojiPercent = this.onChangeEmojiPercent.bind(this);
    }

    changeValue(event) {
        const target_name = event.target.id;
        const target_value = event.target.value;
        const new_states = {};
        new_states[target_name] = target_value;
        this.setState(new_states);
    }

    chooseEmoji(event) {
        const emoji_name = event.target.id;
        var emojies_now = this.state.emoji_now;
        if (emojies_now.includes(emoji_name)) {
            const index = emojies_now.indexOf(emoji_name);
            if (index > -1) {
              emojies_now.splice(index, 1);
            }
        }
        else {
            emojies_now.push(emoji_name)
        }

        this.setState({
            emoji_now: emojies_now
        });
    }


    loadChannelData(channel_data) {
        this.setState({
            view_percent_from: channel_data.view_percent_from,
            view_percent_to: channel_data.view_percent_to,
            channel_reactions: channel_data.channel_reactions
        })
    }

    onChangeEmojiPercent(event) {
        const active_emoji_ids = []
        const input_type = event.target.id
        var channel_reactions_now = this.state.channel_reactions
        var active_emojies = this.state.emoji_now
        var chosen_emojies = []
        console.log(channel_reactions_now)
        for (let i = 0; i < active_emojies.length; i++) {
            for (let j = 0; j < channel_reactions_now.length; j++) {
                if (active_emojies.includes(channel_reactions_now[j]['emoji_type'])){
                    if (!chosen_emojies.includes(channel_reactions_now[j]['emoji_type'])) {
                        active_emoji_ids.push(j)
                        chosen_emojies.push(channel_reactions_now[j]['emoji_type'])
                    }
                }
            }
        }
        for (let i = 0; i < active_emoji_ids.length; i++) {
            if (input_type === "emoji_percent_from"){
                channel_reactions_now[active_emoji_ids[i]]['subscribers_percent_from'] = event.target.value
            }
            else {
                channel_reactions_now[active_emoji_ids[i]]['subscribers_percent_to'] = event.target.value
            }
        }
        this.setState({
            channel_reactions: channel_reactions_now
        })
    }

    async updateChannelSettings() {
        const setNavigateTo = this.props.setNavigateToFunction;
        var percent_sum_from = 0.0
        for (let i = 0; i < this.state.channel_reactions.length; i++) {
            if (this.state.channel_reactions[i]['subscribers_percent_from'] === "") {
                this.state.channel_reactions[i]['subscribers_percent_from'] = 0;
            }
            if (this.state.channel_reactions[i]['subscribers_percent_to'] === "") {
                this.state.channel_reactions[i]['subscribers_percent_to'] = 0;
            }
            percent_sum_from += parseFloat(this.state.channel_reactions[i]['subscribers_percent_from'])
            if (parseFloat(this.state.channel_reactions[i]['subscribers_percent_to']) < parseFloat(this.state.channel_reactions[i]['subscribers_percent_from'])) {
                this.props.updateErrorFunction(true, "Невозможно обновить данные канала так как процент от больше процента до у эмодзи " + this.state.channel_reactions['i']['emoji_type'])
                return;
            }
            if (parseFloat(this.state.channel_reactions[i]['subscribers_percent_to']) > 100) {
                this.props.updateErrorFunction(true, "Невозможно обновить данные канала так как процент до больше 100% у эмодзи " + this.state.channel_reactions['i']['emoji_type'])
                return;
            }
            if (parseFloat(this.state.channel_reactions[i]['subscribers_percent_from']) > 100) {
                this.props.updateErrorFunction(true, "Невозможно обновить данные канала так как процент от больше 100% у эмодзи " + this.state.channel_reactions['i']['emoji_type'])
                return;
            }
        }

        if (percent_sum_from > 100) {
            this.props.updateErrorFunction(true, "Невозможно обновить данные канала тк как общая сумма процентов реакций больше 100%")
            return;
        }

        if (parseFloat(this.state.view_percent_from) > parseFloat(this.state.view_percent_to)) {
            this.props.updateErrorFunction(true, "Невозможно обновить данные канала так как процент просмотров от больше чем процент просмотров до")
            return;
        }


        for (let i = 0; i < this.state.channel_reactions.length; i++) {
            let updateChannelReactionForm = new FormData()
            updateChannelReactionForm.append("channel_emoji_id", this.state.channel_reactions[i]['id'])
            updateChannelReactionForm.append("emoji_percent_from", this.state.channel_reactions[i]['subscribers_percent_from'])
            updateChannelReactionForm.append("emoji_percent_to", this.state.channel_reactions[i]['subscribers_percent_to'])
            updateChannelReactionForm.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
            await axios({
                method: "POST",
                url: "https://api.tgpanel.com.ru/channels/update_channel_emoji_percents",
                data: updateChannelReactionForm
            }).then((response) => {
                if (response.data.error === "Вы не авторизованы") {
                    setNavigateTo("/login")
                }
            })
        }

        const updateChannelViewPercentForm = new FormData()
        updateChannelViewPercentForm.append("channel_id", this.props.channel_id)
        updateChannelViewPercentForm.append("view_percent_from", this.state.view_percent_from)
        updateChannelViewPercentForm.append("view_percent_to", this.state.view_percent_to)
        updateChannelViewPercentForm.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
        await axios({
            method: "POST",
            url: "https://api.tgpanel.com.ru/channels/update_channel_view_percents",
            data: updateChannelViewPercentForm
        }).then((response) => {
            if (response.data.status) {
                this.loadChannelData(response.data.data)
            }
            if (response.data.error === "Вы не авторизованы") {
                setNavigateTo("/login")
            }
        })

        this.props.updateGoodFunction(true, "Данные успешно обновлены")
        setTimeout(() => {
            this.props.setNavigateToFunction("/get_channels")
        }, 1000)
    }

    componentDidMount() {
        const getChannelForm = new FormData()
        const setNavigateTo = this.props.setNavigateToFunction;
        getChannelForm.append("channel_id", this.props.channel_id)
        getChannelForm.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
        axios({
            method: "POST",
            url: "https://api.tgpanel.com.ru/channels/get_one",
            data: getChannelForm
        }).then((response) => {
            if (response.data.status) {
                this.loadChannelData(response.data.data)
            }
            if (response.data.error === "Вы не авторизованы") {
                setNavigateTo("/login")
            }
        })
    }


    render() {
        const emojie_buttons = []
        const emojie_dicts = {
            "🤮": Emoje1,
            "🤯": Emoje2,
            "🎉": Emoje3,
            "🔥": Emoje4,
            "😱": Emoje5,
            "🤬": Emoje6,
            "💩": Emoje7,
            "🙏": Emoje8,
            "❤️": Emoje9,
            "🥰": Emoje10,
            "🤩": Emoje11,
            "👍": Emoje12,
            "👎": Emoje13,
            "👏": Emoje14,
            "🥲": Emoje15,
            "😁": Emoje16,
            "🤔": Emoje17
        }
        const added_keys = []
        for (let i = 0; i < this.state.channel_reactions.length; i++) {
            if (!added_keys.includes(this.state.channel_reactions[i]['emoji_type'])) {
                emojie_buttons.push({
                    "name": this.state.channel_reactions[i]['emoji_type'],
                    "icon": emojie_dicts[this.state.channel_reactions[i]['emoji_type']],
                    "additional_text": this.state.channel_reactions[i]['subscribers_percent_from'] + "% - " +
                        this.state.channel_reactions[i]['subscribers_percent_to'] + "%"
                })
                added_keys.push(this.state.channel_reactions[i]['emoji_type'])
            }
        }
        return <div className="main-data">
            <h1 className="header">Настройки канала {this.state.channel_name}</h1>
            <div className="form">
                <div className="form-input-with-label" key="view_percent_from">
                    <span>
                        Процент просмотров от
                    </span>
                    <input
                        id="view_percent_from"
                        onChange={this.changeValue}
                        type="number" min="0" max="100" step="0.00001" value={this.state.view_percent_from}/>
                </div>
                <div className="form-input-with-label" key="view_percent_to">
                    <span>
                        Процент просмотров до
                    </span>
                    <input
                        id="view_percent_to"
                        onChange={this.changeValue}
                        type="number" min="0" max="100" step="0.00001" value={this.state.view_percent_to}/>
                </div>
                <div className="form-input-with-label" key="emoji-type">
                    <span>
                        Тип реакции
                    </span>
                    <ChooseInput
                        choose_buttons={emojie_buttons}
                        chooseFunction={this.chooseEmoji}
                        chosen_type={this.state.emoji_now}
                        is_multiple={true}
                    />
                </div>
                <div className="form-input-with-label" key="emoji_percent_from">
                    <span>
                        Процент реакции от
                    </span>
                    <input
                        id="emoji_percent_from"
                        onChange={this.onChangeEmojiPercent}
                        type="number" min="0" max="100" step="0.00001"/>
                </div>
                <div className="form-input-with-label" key="emoji_percent_to">
                    <span>
                        Процент реакции до
                    </span>
                    <input
                        id="emoji_percent_to"
                        onChange={this.onChangeEmojiPercent}
                        type="number" min="0" max="100" step="0.00001"/>
                </div>
                <button className="button" onClick={this.updateChannelSettings}>
                    Обновить настройки канала
                </button>
            </div>
        </div>
    }

}


class ChannelElement extends React.Component {
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
                <ChannelEditForm updateGoodFunction={this.updateGood} updateErrorFunction={this.updateError}
                                 setNavigateToFunction={this.setNavigateTo} channel_id={this.props.channel_id} />
            </div>
        );
    }
}

function ChannelPage() {
    let { channel_id } = useParams();
    return <ChannelElement channel_id={channel_id}/>
}


export default ChannelPage