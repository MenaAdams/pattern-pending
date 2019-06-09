class SearchFilter extends React.Component {
  constructor() {
    super();

    this.state = { activeForm: "", searchType: ""};
    this.handleFormClick = this.handleFormClick.bind(this);
    this.handleTypeClick = this.handleTypeClick.bind(this);
  }

  handleFormClick(evt) {
    const activeForm = evt.target.value;
    this.setState({activeForm: activeForm});
    console.log(activeForm);
  }

  handleTypeClick(evt) {
    const searchType = evt.target.value;
    this.setState({searchType: searchType});
    console.log(searchType);
  }

  render() {
    const yarns = ['lace', 'fingering', 'sport', 'dk', 'worsted', 'bulky']; 
    const yarnOptions = [];
    for (const yarn of yarns) {
      const option = <option key={yarn} value={yarn} className="yarn-weight">{yarn}</option>;
      yarnOptions.push(option);
    }
    const patternTypes = ['slippers', 'socks', 'hat', 'gloves', 'mittens', 
                        ['fingerless','fingerless gloves'],'purse', 'cowl', 'scarf', 
                        ['shawl-wrap', 'shawl'], 'blanket', 'pullover', 'cardigan'];
    const patternOptions = [];
    for (const pType of patternTypes) {
      if (typeof pType === 'string') {
        const option = <option key={pType} value={pType} className="pattern_type">{pType}</option>;
        patternOptions.push(option);
      } else {
        const option = <option key={pType[0]} value={pType[0]} className="pattern_type">{pType[1]}</option>;
        patternOptions.push(option);
      }
    }

    return (       
      <div id="root">
        <button
          className="patt-button"
          value="pattern"
          onClick={this.handleTypeClick}>
        Patterns
        </button>
        <button
          className="proj-button"
          value="project"
          onClick={this.handleTypeClick}>
        Projects
        </button>
        <br/>
        <button 
          className="yarn-weight" value="yarn-dropdown" 
          hidden={this.state.searchType === ""}
          onClick={this.handleFormClick}
        >
        Yarn Weight!
        </button>
        <button 
          className="yarn-brand" value="yarn-brand" 
          hidden={this.state.searchType !== "project"}
          onClick={this.handleFormClick}
          >
        Yarn Brand!
        </button>
        <button 
          className="patt-type-button" value="pattern-dropdown"
          hidden={this.state.searchType === ""}
          onClick={this.handleFormClick}
        >
        Item!
        </button>
        <button 
          id="search-w-both" value="both"
          hidden={this.state.searchType === ""}
          onClick={this.handleFormClick}
        >
        Yarn Weight & Item!
        </button>
        <form action="/search-data" id="search-patterns" 
          hidden={this.state.activeForm === ""}>

          <input name="search-type" type="radio" value={this.state.searchType}
          checked hidden readOnly />

          <div
            id="yarn-dropdown"
            hidden={this.state.activeForm === 'pattern-dropdown' || this.state.activeForm === 'yarn-brand'}
          >
            <h2 className="yarn">What kind of yarn do you want to use?</h2>
            <select name="yarn" className="yarn">
              <option value="">Yarn</option>
              {yarnOptions}
            </select>
          </div>

          <div
            id="yarn-brand"
            hidden={this.state.activeForm !== 'yarn-brand'}
          >
            <h2 className="yarn">What brand of yarn do you want to use?</h2><br/>
            <input name="yarn-brand" type="text" className="yarn-brand"/>
          </div>

          <div 
            id="pattern_dropdown"
            hidden={this.state.activeForm === 'yarn-dropdown' || this.state.activeForm === 'yarn-brand'} 
          >
            <h2 className="pattern_type">What kind of item do you want to make?</h2>
            <select name="pattern_type" className="pattern_type">
              <option value="">Item</option>
              {patternOptions}
            </select>
          </div>

          <input type="submit"/>
        </form>
      </div>
    );
  }
}


ReactDOM.render(
  <SearchFilter />,
  document.getElementById("root")
);