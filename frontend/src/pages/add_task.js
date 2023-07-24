import React from "react";
import axios from "axios";
import "../static/css/form.css";
import HeaderComponent from "../components/header";

import ChooseArrow from "../static/img/arrow.svg";


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
import get_cookie from "../functions/get_cookie";
import {Navigate} from "react-router-dom";
import ErrorComponent from "../components/error";
import GoodComponent from "../components/good";
import ChooseInput from "../components/choose_input";

class ChannelInput extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            is_open: this.props.is_open
        }

        this.channelInputChoices = React.createRef();
        this.channelLinkInput = React.createRef();
        this.chooseArrow = React.createRef();


        this.openCloseChoices = this.openCloseChoices.bind(this);
        this.addChannel = this.addChannel.bind(this);
    }


    openCloseChoices(event) {
        if (this.channelInputChoices.current.style.display === "none") {
            this.channelInputChoices.current.style.display = "flex";
            event.target.style.borderRadius = "8px 8px 0px 0px";
        }
        else {
            this.channelInputChoices.current.style.display = "none";
            event.target.style.borderRadius = "8px";
        }
    }

    addChannel() {
        this.props.addChannelFunction(
            this.channelLinkInput.current.value
        );
    }

    render() {
        const changeChannelFunction = this.props.chooseChannelFunction
        const channelsItems = this.props.channels.map((channel, index) => {
            return (
                <button id={"button_" + index} key={channel['link']} className="channel-choice" onClick={changeChannelFunction}>
                  <div id={"button_" + index} className="channel-choice-item">
                      <div id={"button_" + index} className="channel-status"/>
                      <div id={"button_" + index} className="channel-data">
                          <span id={"button_" + index}>{channel['name']}</span>
                          <a className="channel-link" href={channel['link']}>{channel['link']}</a>
                      </div>
                  </div>
              </button>
            );
        })
        return (
          <div className="channel-input">
              <button className="channel-input-main" onClick={this.openCloseChoices}>
                  <span>{this.props.channel_id === -1 ? "Выберите канал или добавьте" : this.props.channels[this.props.channel_id]['name']}</span>
                  <div className="choose-arrow">
                      <img src={ChooseArrow} alt="choose-arrow"  ref={this.chooseArrow} />
                  </div>
              </button>
              <div className="channel-input-choices" ref={this.channelInputChoices} style={{
                  "display": "none"
              }}>
                  <div className="channel-input-add">
                      <input placeholder="Ссылка на канал" ref={this.channelLinkInput}/>
                      <button onClick={this.addChannel}>
                          Добавить
                      </button>
                  </div>
                  {channelsItems}
              </div>
          </div>
        );
    }
}


class InputWithChoose extends React.Component {
    constructor(props) {
        super(props);
    }


    render() {
        const chosenName = this.props.chosenName;
        const chooseFunction = this.props.chooseFunction;
        const buttonsItems = this.props.buttons.map((button) => {
            return <button id={button['name']} key={button['name']} className={button['name'] === chosenName ? "chosen" : ""} onClick={chooseFunction}>
                {button['text']}
            </button>
        });
        var typeInput = this.props.type
        if (this.props.type === undefined || this.props.type === null) {
            typeInput = "number"
        }
        return (
            <div className="input-with-variants">
                <input id={this.props.target_id} type={typeInput} placeholder={this.props.placeholder} onChange={this.props.changeValueFunction} />
                <div className="variants">
                    {buttonsItems}
                </div>
            </div>
        );
    }

}


class AddTasksForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            task_name: "",
            task_now: "subscribers",
            channels: [],
            speed_type: "minutes",
            speed_value: 1,
            timer_type: "minutes",
            timer_value: 1,
            count_make: 0,
            emoji_now: [],
            percent_active_subscribers: 0,
            percent_moment_unsubscribes: 0,
            percent_t_unsubscribes: 0,
            read_last_posts: false,
            floating_speed: false,
            percent_returned: false,
            posts_ids: "",
            only_subscribers: false,
            comment_text: "",
            repeat_comments: false,
            vote_number: 0,
            channel_id: -1,
            profile_type: "user",
            profile_link: ""
        }
        this.chooseTask = this.chooseTask.bind(this);
        this.chooseEmoji = this.chooseEmoji.bind(this);
        this.chooseSpeedType = this.chooseSpeedType.bind(this);
        this.chooseTimerType = this.chooseTimerType.bind(this);
        this.addChannel = this.addChannel.bind(this);
        this.changeValue = this.changeValue.bind(this);
        this.changeCheckbox = this.changeCheckbox.bind(this);
        this.chooseChannelId = this.chooseChannelId.bind(this);
        this.createTask = this.createTask.bind(this);
        this.updateChannels = this.updateChannels.bind(this);
        this.chooseVkProfileType = this.chooseVkProfileType.bind(this);
    }

    chooseTask(event) {
        const task_name = event.target.id;
        this.setState({
            task_now: task_name
        });
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

    chooseSpeedType(event) {
        const speed_name = event.target.id
        this.setState({
            speed_type: speed_name
        })
    }

    chooseTimerType(event) {
        const timer_name = event.target.id;
        this.setState({
            timer_type: timer_name
        });
    }

    chooseVkProfileType(event) {
        const profile_type = event.target.id;
        this.setState({
            profile_type: profile_type
        });
    }

    chooseChannelId(event) {
        const chosenChannelId = event.target.id.split("_")[1];
        this.setState({
            channel_id: chosenChannelId
        });
    }

    changeValue(event) {
        const target_name = event.target.id;
        const target_value = event.target.value;
        const new_states = {};
        new_states[target_name] = target_value;
        this.setState(new_states);
    }

    changeCheckbox(event) {
        const target_name = event.target.id;
        const target_checked = event.target.checked;
        const new_states = {};
        new_states[target_name] = target_checked;
        this.setState(new_states);
    }


    addChannel(link) {
        const form = new FormData();
        form.append("channel_link", link);
        form.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
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

    updateChannels() {
        const form = new FormData()
        form.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
        axios({
            method: "POST",
            url: "https://api.tgpanel.com.ru/channels/get_all",
            data: form
        }).then((response) => {
            if (response.data.status) {
                const channels = []
                for (let i = 0; i < response.data.data.length; i++) {
                    channels.push({
                        "name": response.data.data[i].channel_name,
                        "link": response.data.data[i].channel_invite_link,
                    });
                }
                this.setState({
                    channels: channels
                });
            }
            if (response.data.error === "Вы не авторизованы") {
                this.props.setNavigateToFunction("/login")
            }
        });
    }

    async createTask() {
        const task_name = this.state.task_name;
        const task_now = this.state.task_now;
        const channels = this.state.channels;
        const speed_type = this.state.speed_type;
        const speed_value = this.state.speed_value;
        const timer_type = this.state.timer_type;
        const timer_value = this.state.timer_value;
        const count_make  = this.state.count_make;
        const emoji_now = this.state.emoji_now;
        const percent_active_subscribers = this.state.percent_active_subscribers;
        const percent_moment_unsubscribes = this.state.percent_moment_unsubscribes;
        const percent_t_unsubscribes = this.state.percent_t_unsubscribes;
        const read_last_posts = this.state.read_last_posts;
        const floating_speed = this.state.floating_speed;
        const percent_returned = this.state.percent_returned;
        const posts_ids = this.state.posts_ids;
        const only_subscribers = this.state.only_subscribers;
        const comment_text = this.state.comment_text;
        const repeat_comments = this.state.repeat_comments;
        const vote_number = this.state.vote_number;
        const channel_id = this.state.channel_id;
        const profile_type = this.state.profile_type;
        const profile_link = this.state.profile_link;
        const current = new Date();
        var startTime = new Date(current.getTime() + 60000 * parseInt(timer_value) * (timer_type === "minutes" ? 1 : 60));
        var endTime = new Date(current.getTime() + 60000 * parseInt(timer_value) * (timer_type === "minutes" ? 1 : 60) + 60000
            * parseInt(speed_value) * (speed_type === "minutes" ? 1 : 60));
        var date = startTime.getFullYear()+'-'+(startTime.getMonth()+1)+'-'+startTime.getDate();
        var time = startTime.getHours()+':'+startTime.getMinutes()+':'+startTime.getSeconds();
        startTime = date + " " + time
        date = endTime.getFullYear()+'-'+(endTime.getMonth()+1)+'-'+endTime.getDate();
        time = endTime.getHours()+':'+endTime.getMinutes()+':'+endTime.getSeconds();
        endTime = date + " " + time
        const taskArguments = {
            "task_name": task_name,
            "task_now": task_now,
            "start_t": startTime,
            "end_t": endTime,
            "count_make": count_make,
            "emoji_now": emoji_now,
            "percent_active_subscribers": percent_active_subscribers,
            "percent_moment_unsubscribes": percent_moment_unsubscribes,
            "percent_t_unsubscribes": percent_t_unsubscribes,
            "read_last_posts": read_last_posts,
            "floating_speed": floating_speed,
            "percent_returned": percent_returned,
            "posts_ids": posts_ids,
            "only_subscribers": only_subscribers,
            "comment_text": comment_text,
            "repeat_comments": repeat_comments,
            "vote_number": vote_number,
            "channel_link": channels[channel_id],
            "profile_type": profile_type,
            "profile_link": profile_link
        };
        if (taskArguments["channel_link"] !== undefined && taskArguments['channel_link'] !== null) {
            taskArguments['channel_link'] = taskArguments['channel_link']['link']
        }

        const subscribersRequiredArguments = [
            "start_t",
            "end_t",
            "percent_moment_unsubscribes",
            "percent_t_unsubscribes",
            "read_last_posts",
            "floating_speed",
            "channel_link"
        ];

        const removeSubscribersRequiredArguments = [
            "start_t",
            "end_t",
            "percent_returned",
            "floating_speed",
            "channel_link"
        ];

        const viewsRequiredArguments = [
            "start_t",
            "end_t",
            "posts_ids",
            "only_subscribers",
            "floating_speed",
            "channel_link"
        ];

        const reactionsRequiredArguments = [
            "start_t",
            "end_t",
            "posts_ids",
            "emoji_now",
            "only_subscribers",
            "floating_speed",
            "channel_link"
        ];

        const votesRequiredArguments = [
            "start_t",
            "end_t",
            "posts_ids",
            "vote_number",
            "only_subscribers",
            "floating_speed",
            "channel_link"
        ];

        const commentsRequiredArguments = [
            "start_t",
            "end_t",
            "posts_ids",
            "comment_text",
            "only_subscribers",
            "repeat_comments",
            "floating_speed",
            "channel_link"
        ];

        const vkRequiredArguments = [
            "start_t",
            "profile_type",
            "profile_link"
        ]
        var reqArguments = [];
        if (task_now === "subscribers") {
            reqArguments = subscribersRequiredArguments;
        }
        else if (task_now === "remove_subscribers") {
            reqArguments = removeSubscribersRequiredArguments;
        }
        else if (task_now === "views") {
            reqArguments = viewsRequiredArguments;
        }
        else if (task_now === "reactions") {
            reqArguments = reactionsRequiredArguments;
        }
        else if (task_now === "votes") {
            reqArguments = votesRequiredArguments;
        }
        else if (task_now === "comments") {
            reqArguments = commentsRequiredArguments;
        }
        else if (task_now === "parse_vk") {
            reqArguments = vkRequiredArguments;
        }
        for (let i = 0; i < reqArguments.length; i++) {
            if (taskArguments[reqArguments[i]] === undefined || taskArguments[reqArguments[i]] === null || taskArguments[reqArguments[i]] === "undefined" || taskArguments[reqArguments[i]] === "" || taskArguments[reqArguments[i]] < 0) {
                this.props.updateErrorFunction(
                    true,
                    "Заполнены не все данные"
                )
                return;
            }
        }
        const setNavigateTo = this.props.setNavigateToFunction
        if (reqArguments.includes("emoji_now")) {
            for (let ei = 0; ei < taskArguments['emoji_now'].length; ei++) {
                const emoji_idx = ei
                console.log(taskArguments['emoji_now'][ei])
                const taskForm = new FormData();
                taskForm.append("task_model_name", this.state.task_name);
                taskForm.append("task_model_type", this.state.task_now);
                taskForm.append("task_model_required_count", parseInt(this.state.count_make));
                taskForm.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
                console.log("CREATE")
                if (this.state.task_name !== "" && this.state.task_now !== "" && (parseInt(this.state.count_make) > 0 || this.state.task_now === "parse_vk")) {
                    await axios({
                        method: "POST",
                        url: "https://api.tgpanel.com.ru/task/create",
                        data: taskForm
                    }).then(async (response) => {
                        if (response.data.status) {
                            for (let i = 0; i < reqArguments.length; i++) {
                                if (reqArguments[i] !== "emoji_now") {
                                    let form_task_argument = new FormData();
                                    form_task_argument.append("task_argument_model_name", reqArguments[i]);
                                    form_task_argument.append("task_argument_model_value", taskArguments[reqArguments[i]]);
                                    form_task_argument.append("task_argument_model_task_id", response.data.data);
                                    form_task_argument.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
                                    await axios({
                                        method: "POST",
                                        url: "https://api.tgpanel.com.ru/task_argument/create",
                                        data: form_task_argument
                                    });
                                }
                                else {
                                    let form_task_argument = new FormData();
                                    form_task_argument.append("task_argument_model_name", reqArguments[i]);
                                    form_task_argument.append("task_argument_model_value", taskArguments[reqArguments[i]][emoji_idx]);
                                    form_task_argument.append("task_argument_model_task_id", response.data.data);
                                    form_task_argument.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
                                    await axios({
                                        method: "POST",
                                        url: "https://api.tgpanel.com.ru/task_argument/create",
                                        data: form_task_argument
                                    });
                                }
                            }
                        }
                        if (response.data.error === "Вы не авторизованы") {
                            this.props.setNavigateToFunction("/login")
                        }
                    })
                }
            }
            this.props.updateGoodFunction(true, "Задача успешно создана")
            setTimeout(() => {
                setNavigateTo("/get_tasks")
            }, 1000)
        }
        else {
            const taskForm = new FormData();
            taskForm.append("task_model_name", this.state.task_name);
            taskForm.append("task_model_type", this.state.task_now);
            taskForm.append("task_model_required_count", parseInt(this.state.count_make));
            taskForm.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
            if (this.state.task_name !== "" && this.state.task_now !== "" && (parseInt(this.state.count_make) > 0 || this.state.task_now === "parse_vk")) {
                axios({
                    method: "POST",
                    url: "https://api.tgpanel.com.ru/task/create",
                    data: taskForm
                }).then(async (response) => {
                    if (response.data.status) {
                        for (let i = 0; i < reqArguments.length; i++) {
                            let form_task_argument = new FormData();
                            form_task_argument.append("task_argument_model_name", reqArguments[i]);
                            form_task_argument.append("task_argument_model_value", taskArguments[reqArguments[i]]);
                            form_task_argument.append("task_argument_model_task_id", response.data.data);
                            form_task_argument.append("admin_login_session_model_session_hash", get_cookie("session_hash"))
                            await axios({
                                method: "POST",
                                url: "https://api.tgpanel.com.ru/task_argument/create",
                                data: form_task_argument
                            });
                        }
                        this.props.updateGoodFunction(true, "Задача успешно создана")
                        setTimeout(() => {
                            setNavigateTo("/get_tasks")
                        }, 1000)
                    }
                    if (response.data.error === "Вы не авторизованы") {
                        this.props.setNavigateToFunction("/login")
                    }
                })
            }
        }
    }

    componentDidMount() {
        this.updateChannels()
    }

    render() {
        let additionalInputs = undefined
        const subscribersInputs = [
                (
                    <div className="form-input-with-label" key="percent-moment-unsubscribes">
                        <span>
                            Процент моментальных отписок
                        </span>
                        <input id="percent_moment_unsubscribes"
                               onChange={this.changeValue} type="number" min="0" max="100" />
                    </div>
                ),
                (
                    <div className="form-input-with-label" key="percent-timer-unsubscribes">
                        <span>
                            Процент отписок через время
                        </span>
                        <input id="percent_t_unsubscribes"
                               onChange={this.changeValue} type="number" min="0" max="100" />
                    </div>
                ),
                (
                    <div className = "form-checkbox-with-label" key="read-last-posts">
                        <input id="read_last_posts" onChange={this.changeCheckbox} type="checkbox"/>
                        <label htmlFor="read_last_posts"></label>
                        <span>Чтение последних постов при добавлении</span>
                    </div>
                ),
                (
                    <div className = "form-checkbox-with-label" key="floating-speed">
                        <input id="floating_speed" onChange={this.changeCheckbox} type="checkbox" />
                        <label htmlFor="floating_speed"></label>
                        <span>Плавающая скорость добавления</span>
                    </div>
                )
            ]
        const removeSubscribersInputs= [
                    (
                        <div className="form-input-with-label" key="percent-returned">
                            <span>
                                Процент возврата через время
                            </span>
                            <input
                                id="percent_returned"
                                onChange={this.changeValue}
                                type="number" min="0" max="100" />
                        </div>
                    ),
                    (
                        <div className = "form-checkbox-with-label" key="floating-speed">
                            <input id="floating_speed" onChange={this.changeCheckbox} type="checkbox"/>
                            <label htmlFor="floating_speed"></label>
                            <span>Плавающая скорость отписок</span>
                        </div>
                    )
                ]
        const viewsInputs = [
                    (
                        <div className="form-input-with-label" key="posts-ids">
                            <span>
                                ID или ссылки постов для накрутки через перенос строки
                            </span>
                            <textarea id="posts_ids"
                                onChange={this.changeValue} />
                        </div>
                    ),
                    (
                        <div className = "form-checkbox-with-label" key="only-subscribers">
                            <input id="only_subscribers" onChange={this.changeCheckbox} type="checkbox"/>
                            <label htmlFor="only_subscribers"></label>
                            <span>Только подписчики</span>
                        </div>
                    ),
                    (
                        <div className = "form-checkbox-with-label" key="floating-speed">
                            <input id="floating_speed" onChange={this.changeCheckbox} type="checkbox"/>
                            <label htmlFor="floating_speed"></label>
                            <span>Плавающая скорость добавления</span>
                        </div>
                    )
                ]
        const reactionsInputs = [
                        (
                        <div className="form-input-with-label" key="posts-ids">
                            <span>
                                ID или ссылки постов для накрутки через перенос строки
                            </span>
                            <textarea id="posts_ids"
                                onChange={this.changeValue} />
                        </div>
                        ),
                        (
                            <div className="form-input-with-label" key="emoji-type">
                                <span>
                                    Тип реакции
                                </span>
                                <ChooseInput
                                    choose_buttons={[
                                        {
                                            "name": "🤮",
                                            "icon": Emoje1
                                        },
                                        {
                                            "name": "🤯",
                                            "icon": Emoje2
                                        },
                                        {
                                            "name": "🎉",
                                            "icon": Emoje3
                                        },
                                        {
                                            "name": "🔥",
                                            "icon": Emoje4
                                        },
                                        {
                                            "name": "😱",
                                            "icon": Emoje5
                                        },
                                        {
                                            "name": "🤬",
                                            "icon": Emoje6
                                        },
                                        {
                                            "name": "💩",
                                            "icon": Emoje7
                                        },
                                        {
                                            "name": "🙏",
                                            "icon": Emoje8
                                        },
                                        {
                                            "name": "❤️",
                                            "icon": Emoje9
                                        },
                                        {
                                            "name": "🥰",
                                            "icon": Emoje10
                                        },
                                        {
                                            "name": "🤩",
                                            "icon": Emoje11
                                        },
                                        {
                                            "name": "👍",
                                            "icon": Emoje12
                                        },
                                        {
                                            "name": "👎",
                                            "icon": Emoje13
                                        },
                                        {
                                            "name": "👏",
                                            "icon": Emoje14
                                        },
                                        {
                                            "name": "🥲",
                                            "icon": Emoje15
                                        },
                                        {
                                            "name": "😁",
                                            "icon": Emoje16
                                        },
                                        {
                                            "name": "🤔",
                                            "icon": Emoje17
                                        },
                                    ]}
                                    chooseFunction={this.chooseEmoji}
                                    chosen_type={this.state.emoji_now}
                                    is_multiple={true}
                                />
                            </div>
                        ),
                        (
                            <div className = "form-checkbox-with-label" key="only-subscribers">
                                <input id="only_subscribers" onChange={this.changeCheckbox} type="checkbox"/>
                                <label htmlFor="only_subscribers"></label>
                                <span>Только подписчики</span>
                            </div>
                        ),
                        (
                            <div className = "form-checkbox-with-label" key="floating-speed">
                                <input id="floating_speed" onChange={this.changeCheckbox} type="checkbox"/>
                                <label htmlFor="floating_speed"></label>
                                <span>Плавающая скорость добавления</span>
                            </div>
                        )
                    ]
        const votesInputs = [
            (
                <div className="form-input-with-label" key="posts-ids">
                    <span>
                        ID или ссылки постов для накрутки через перенос строки
                    </span>
                    <textarea id="posts_ids"
                                onChange={this.changeValue}  />
                </div>
            ),
            (
                <div className="form-input-with-label" key="vote_number">
                    <span>Номер вопроса</span>
                    <input id="vote_number"
                                onChange={this.changeValue} type="number" min="1"/>
                </div>
            ),
            (
                <div className = "form-checkbox-with-label" key="only-subscribers">
                    <input id="only_subscribers" type="checkbox" onChange={this.changeCheckbox}/>
                    <label htmlFor="only_subscribers"></label>
                    <span>Только подписчики</span>
                </div>
            ),
            (
                <div className = "form-checkbox-with-label" key="floating-speed">
                    <input id="floating_speed" type="checkbox" onChange={this.changeCheckbox}/>
                    <label htmlFor="floating_speed"></label>
                    <span>Плавающая скорость добавления</span>
                </div>
            )
        ]
        const commentsInputs = [
            (
                <div className="form-input-with-label" key="posts-ids">
                    <span>
                        ID или ссылки постов для накрутки через перенос строки
                    </span>
                    <textarea id="posts_ids"
                                onChange={this.changeValue} />
                </div>
            ),
            (
                <div className="form-input-with-label" key="comments">
                    <span>Текст комментариев</span>
                    <textarea id="comment_text" onChange={this.changeValue} placeholder={"Текст\nкомментария 1|Текст комментария 2|Текст комментария 3"}>
                    </textarea>
                </div>
            ),
            (
                <div className = "form-checkbox-with-label" key="only-subscribers">
                    <input id="only_subscribers" type="checkbox" onChange={this.changeCheckbox}/>
                    <label htmlFor="only_subscribers"></label>
                    <span>Только подписчики</span>
                </div>
            ),
            (
                <div className = "form-checkbox-with-label" key="repeat-comments">
                    <input id="repeat_comments" type="checkbox" onChange={this.changeCheckbox}/>
                    <label htmlFor="repeat_comments"></label>
                    <span>Повторять текст комментария</span>
                </div>
            ),
            (
                <div className = "form-checkbox-with-label" key="floating-speed" onChange={this.changeCheckbox}>
                    <input id="floating_speed" type="checkbox"/>
                    <label htmlFor="floating_speed"></label>
                    <span>Плавающая скорость добавления</span>
                </div>
            )
        ]

        const parseVkInputs = [
            <div className="form-input-with-label" key="link-vk">
                <span>
                    Ссылка на профиль вк
                </span>
                <InputWithChoose
                    target_id="profile_link"
                    chosenName={this.state.profile_type}
                    placeholder="Введите ссылку"
                    changeValueFunction={this.changeValue}
                    type="text"
                    buttons={[
                        {
                            "name": "user",
                            "text": "Пользователь"
                        },
                        {
                            "name": "channel",
                            "text": "Группа"
                        }
                    ]}
                    chooseFunction={this.chooseVkProfileType}
                />
            </div>,

        ]
        if (this.state.task_now === "subscribers") {
            additionalInputs = subscribersInputs
        }
        else if (this.state.task_now === "remove_subscribers") {
            additionalInputs = removeSubscribersInputs
        }
        else if (this.state.task_now === "views") {
            additionalInputs = viewsInputs
        }
        else if (this.state.task_now === "reactions") {
            additionalInputs = reactionsInputs
        }
        else if (this.state.task_now === "votes") {
            additionalInputs = votesInputs
        }
        else if (this.state.task_now === "comments") {
            additionalInputs = commentsInputs
        }

        var main_inputs = [
            <div className="form-input-with-label" key="channel-link">
                        <span>
                            Канал
                        </span>
                        <ChannelInput
                            channels = {this.state.channels}
                            addChannelFunction={this.addChannel}
                            chooseChannelFunction={this.chooseChannelId}
                            channel_id={this.state.channel_id}
                        />
                    </div>,
                    <div className="form-input-with-label" key = "req-count">
                        <span>
                            Количество действий
                        </span>
                        <input id="count_make" type="number" min="1" value={this.count_make} onChange={this.changeValue}/>
                    </div>,
                    <div className="form-input-with-label" key="speed">
                        <span>
                            Скорость накрутки
                        </span>
                        <InputWithChoose
                            target_id="speed_value"
                            chosenName={this.state.speed_type}
                            placeholder="Введите количество"
                            changeValueFunction={this.changeValue}
                            buttons={[
                                {
                                    "name": "minutes",
                                    "text": "Минуты"
                                },
                                {
                                    "name": "hours",
                                    "text": "Часы"
                                }
                            ]}
                            chooseFunction={this.chooseSpeedType}
                        />
                    </div>,
                    <div className="form-input-with-label" key="timer">
                        <span>
                            Запустить задачу через
                        </span>
                        <InputWithChoose
                            target_id="timer_value"
                            chosenName={this.state.timer_type}
                            placeholder="Введите количество"
                            changeValueFunction={this.changeValue}
                            buttons={[
                                {
                                    "name": "minutes",
                                    "text": "Минуты"
                                },
                                {
                                    "name": "hours",
                                    "text": "Часы"
                                }
                            ]}
                            chooseFunction={this.chooseTimerType}
                        />
                    </div>
        ]
        if (this.state.task_now === "parse_vk") {
            main_inputs = parseVkInputs;
        }


        return (
            <div className="main-data">
                <h1 className="header">Оформить задачу</h1>
                <div className="form">
                    <div className="form-input-with-label">
                        <span>
                            Название задачи
                        </span>
                        <input id="task_name" type="text" value={this.state.task_name} onChange={this.changeValue}/>
                    </div>
                    <div className="form-input-with-label">
                        <span>
                            Тип задачи
                        </span>
                        <ChooseInput
                            choose_buttons = {[
                                {
                                    "name": "subscribers",
                                    "text": "Подписчики"
                                },
                                {
                                    "name": "remove_subscribers",
                                    "text": "Отписка"
                                },
                                {
                                    "name": "views",
                                    "text": "Просмотры"
                                },
                                {
                                    "name": "reactions",
                                    "text": "Реакции"
                                },
                                {
                                    "name": "votes",
                                    "text": "Голосование"
                                },
                                {
                                    "name": "comments",
                                    "text": "Комментариии"
                                },
                                {
                                    "name": "parse_vk",
                                    "text": "Парсинг VK"
                                }
                            ]}
                            chosen_type = {this.state.task_now}
                            chooseFunction = {this.chooseTask}
                        />
                    </div>
                    {main_inputs}
                    {additionalInputs}
                    <button className="button" onClick={this.createTask}>
                        Оформить задачу
                    </button>
                </div>
            </div>
        );
    }
}


class AddTasksPage extends React.Component {
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
                <AddTasksForm updateGoodFunction={this.updateGood} updateErrorFunction={this.updateError}
                                setNavigateToFunction={this.setNavigateTo} />
            </div>
        );
    }
}

export default AddTasksPage