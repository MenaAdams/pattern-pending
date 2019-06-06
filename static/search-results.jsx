class RenderPatterns extends React.Component {
    constructor() {
      super();
      this.state = {
        patterns: [],
        userPatterns: ''
      };
    }

    componentDidMount() {
      console.log("i'm mounting a component!")
      fetch('/search-results.json')
        .then(res => res.json())
        .then(patterns => {
          this.setState({ patterns: patterns });
        });
      fetch('/users-categories.json')
        .then(res => res.json())
        .then(userPatterns => {
          this.setState({ userPatterns: userPatterns});
        console.log(this.state.userPatterns);
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

