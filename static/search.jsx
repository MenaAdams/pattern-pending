class SearchFilter extends React.Component {
  constructor() {
    super();

    this.state = { activeForm: "", searchType: "" };
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

  changeOpacityClick(evt) {

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
        <div id="search-types">
          <button
            className="type-button"
            value="pattern"
            onClick={this.handleTypeClick}
          >
          Patterns
          </button>
          or
          <button
            className="type-button"
            value="project"
            onClick={this.handleTypeClick}
          >
          Projects
          </button>
        </div>
        <br/>
        <div id="search-categories">
          <button 
            className="search-data" value="yarn-dropdown" 
            hidden={this.state.searchType === ""}
            onClick={this.handleFormClick}
          >
          Yarn Weight
          </button>
          <button 
            className="search-data" value="yarn-brand" 
            hidden={this.state.searchType !== "project"}
            onClick={this.handleFormClick}
          >
          Yarn Brand
          </button>
          <button 
            className="search-data" value="pattern-dropdown"
            hidden={this.state.searchType === ""}
            onClick={this.handleFormClick}
          >
          Item
          </button>
          <button 
            className="search-data" value="both"
            hidden={this.state.searchType === ""}
            onClick={this.handleFormClick}
          >
          Yarn & Item
          </button>
        </div>
        <form action="/search-data" id="search-patterns" 
          hidden={this.state.activeForm === ""}>

          <input name="search-type" type="radio" value={this.state.searchType}
          checked hidden readOnly />

          <div
            id="yarn-dropdown"
            hidden={this.state.activeForm === 'pattern-dropdown' || this.state.activeForm === 'yarn-brand'}
          >
            <label for="yarn">Enter Yarn Weight
              <select name="yarn" className="yarn">
                <option value="">Yarn</option>
                {yarnOptions}
              </select>
            </label>
          </div>

          <div
            id="yarn-brand"
            hidden={this.state.activeForm !== 'yarn-brand'}
          >
            <label for="yarn-brand">Enter Yarn Brand
              <input name="yarn-brand" type="text" className="yarn-brand"/>
            </label>
          </div>

          <div 
            id="pattern_dropdown"
            hidden={this.state.activeForm === 'yarn-dropdown' || this.state.activeForm === 'yarn-brand'} 
          >
            <label for="pattern_type">Enter Item
              <select name="pattern_type" className="pattern_type">
                <option value="">Item</option>
                {patternOptions}
              </select>
            </label>
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