import React from "react";

class ChooseInput extends React.Component {
    constructor(props) {
        super(props);
    }



    render() {
        var chosen_types = []
        if (!this.props.is_multiple) {
            chosen_types = [
                this.props.chosen_type,
            ];
        }
        else {
            chosen_types = this.props.chosen_type
        }
        const choose_buttons_items = this.props.choose_buttons.map((choose_button_item) => {
            return <button id={choose_button_item['name']} key={choose_button_item['name']}
                           className={chosen_types.includes(choose_button_item['name']) ? "chosen" : ""}
                           onClick={this.props.chooseFunction}>
                {choose_button_item.text === undefined ? <div id={choose_button_item['name']} className="choose-button-icon" style={{marginLeft: "auto", marginRight: "auto"}}>
                    <img id={choose_button_item['name']} src={choose_button_item.icon} />
                </div> : choose_button_item.text}
                {choose_button_item.additional_text ? <span id={choose_button_item['name']} className="additional_text">{choose_button_item.additional_text}</span> : undefined}
            </button>
        });
        return (
            <div className="choose">
                {choose_buttons_items}
            </div>
        );
    }
}

export default ChooseInput
