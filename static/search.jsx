
class YarnDropdown extends React.Component {
    constructor() {
        super();
        this.state = { value: ''};
    }

    render() {
        return (
        <option className="yarn">{ this.props.yarn }</option>
        this.setState( {value: this.props.yarn})
        );
    }
}

ReactDOM.render(
(
<YarnDropdown yarn="lace"/>
),
document.getElementById('yarn-dropdown')
);

/* const yarns = ['lace', 'fingering', 'sport', 'dk', 'worsted', 'bulky']; */