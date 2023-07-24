import React from "react";
import HeaderComponent from "../components/header";
import Error404Image from "../static/img/404.svg";
import {Link} from "react-router-dom";
import "../static/css/404_error.css";


function Error404Page() {
    return <div>
        <HeaderComponent />
        <div className="main-data">
            <h1 className="header">Что-то пошло не так...</h1>
            <span className="description">Мы надеемся Вы найдете что ищите, возможно был сбой – повторите свой запрос чуть позже.</span>
            <div className="image-404">
                <img alt="404" src={Error404Image}/>
            </div>
            <Link className="button" to="/">
                На главную
            </Link>
        </div>
    </div>
}


export default Error404Page