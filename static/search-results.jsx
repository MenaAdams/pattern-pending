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
          <div id="loading-yarn"></div>
        </div>
        );
      }

      return (
        <div id="search-results">
        <h1>Results!</h1>
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

