class RenderPatterns extends React.Component {
    constructor() {
      super();
      this.state = {patterns: []};
    }

    componentDidMount() {
      fetch('/search-results.json')
        .then(res => res.json())
        .then(patterns => {
          this.setState({patterns: patterns});
        });
    }
  
    render() {
      return (
        <div>
        {this.state.patterns.map(pattern => {
          return (
            <div key={pattern.name} className="pattern">
            <b>{pattern.name}</b><br/>
            <a href={pattern.url}>
            <img src={pattern.photo}/>
            </a>
            </div>
          );
        })}
        </div>
      );
    }
}

ReactDOM.render(
  <RenderPatterns />,
  document.getElementById("root")
);

