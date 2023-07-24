import React from "react";
import ErrorImage from "../static/img/lightbulb.png";
import "../static/css/windows.css";


function ErrorComponent (props) {
    return <div className="window" style={{
        "display": props.is_show ? "flex" : "none"
    }}>
        <div className="image-window">
            <img src={ErrorImage} alt={"error"}/>
        </div>
        <span className="title-window">Произошла ошибка</span>
        <span className="description-window">{props.text}</span>
        <button className="button-window" onClick={props.closeWindowsFunction}>Готово</button>
    </div>
}

export default ErrorComponent