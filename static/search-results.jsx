class RenderPatterns extends React.Component {
    constructor() {
      super();
      this.state = {patterns: [],
                  loading: true};
    }

    componentDidMount() {
      fetch('/search-results.json')
        .then(res => res.json())
        .then(patterns => {
          this.setState({patterns: patterns})
          this.setState({loading: false});
        });

    }
  
    render() {
      const { loading } = this.state;
      if (loading) {
        return (
        <div class="loading">
          <h1>Loading Results</h1>
          <img src="static/loading-cat.svg" />
        </div>
        );
      }

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

