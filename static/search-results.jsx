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
        <div id="search-results">
        {this.state.patterns.map(pattern => {
          return (
            <a href={pattern.url} target="_blank">
              <div key={pattern.name} className="pattern-card">
                <img src={pattern.photo} alt="pattern" />
                <h3>{pattern.name}</h3><br/>
              </div>
            </a>
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

