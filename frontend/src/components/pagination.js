import React from "react";
import Arrow from "../static/img/arrow.svg";

import "../static/css/pagination.css";


class PaginationComponent extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const pages = [];
        const activePage = parseInt(this.props.active_page);
        let count_pages = parseInt(this.props.count_pages);
        let min_page = activePage - 1 === 0 ? activePage : activePage - 1;
        if (count_pages < 10) {
            for (let i = min_page; i < count_pages; i++) {
                pages.push(
                    <button id={i} key={i} className={String(i) === String(activePage) ? "active" : ""}
                            onClick={this.props.changePageFunction}>
                        {i}
                    </button>
                );
            }
        }
        else if (min_page + 8 <= count_pages) {
            count_pages = min_page + 8;
            for (let i = min_page; i < count_pages; i++) {
                pages.push(
                    <button id={i} key={i} className={String(i) === String(activePage) ? "active" : ""}
                            onClick={this.props.changePageFunction}>
                        {i}
                    </button>
                );
            }
        }
        else {
            min_page = count_pages - 8
            for (let i = min_page; i <= count_pages; i++) {
                pages.push(
                    <button id={i} key={i} className={String(i) === String(activePage) ? "active" : ""}
                            onClick={this.props.changePageFunction}>
                        {i}
                    </button>
                );
            }
        }
        if (pages.length) {
            return (
                <div className="pagination">
                    <button
                        id={parseInt(this.props.active_page) - 1 <= 0 ? parseInt(this.props.active_page) : parseInt(this.props.active_page) - 1}
                        className="image-button"
                        onClick={this.props.changePageFunction}
                    >
                        <img
                            id={parseInt(this.props.active_page) + 1 >= parseInt(this.props.count_pages) ? parseInt(this.props.active_page) : parseInt(this.props.active_page) + 1}
                            className="next" alt="arrow" src={Arrow}/>
                    </button>
                    {pages}
                    <button
                        id={parseInt(this.props.active_page) + 1 >= parseInt(this.props.count_pages) ? parseInt(this.props.active_page) : parseInt(this.props.active_page) + 1}
                        className="image-button"
                        onClick={this.props.changePageFunction}
                    ><img
                        id={parseInt(this.props.active_page) + 1 >= parseInt(this.props.count_pages) ? parseInt(this.props.active_page) : parseInt(this.props.active_page) + 1}
                        className="prev" alt="arrow" src={Arrow}/></button>
                </div>
            );
        }
        else {
            return (<div className="pagination"></div>)
        }
    }
}

export default PaginationComponent
