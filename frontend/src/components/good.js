import React from "react";
import GoodImage from "../static/img/fire.png";
import "../static/css/windows.css";
import ErrorImage from "../static/img/lightbulb.png";

function GoodComponent (props) {
    return <div className="window" style={{
        "display": props.is_show ? "flex" : "none"
    }}>
        <div className="image-window">
            <img src={ErrorImage} alt={"error"}/>
        </div>
        <span className="title-window">Действие успешно выполнено</span>
        <span className="description-window">{props.text}</span>
        <button className="button-window" onClick={props.closeWindowsFunction}>Понятно</button>
    </div>
}

export default GoodComponent
