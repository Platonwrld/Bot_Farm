import React from "react";
import Logo from "../static/img/logo.svg";

import "../static/css/header.css";
import {Link} from "react-router-dom";

class HeaderComponent extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (<div className="main-header">
            <Link to="/dashboard" className="logo">
                <img src={Logo} alt="Logo"/>
            </Link>
        </div>);
    }

}
export default HeaderComponent