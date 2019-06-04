
class SearchFilter extends React.Component {
  constructor() {
    super();

    this.state = { activeForm: ""};
    this.handleClick = this.handleClick.bind(this);
  }

  handleClick(evt) {
    const activeForm = evt.target.value;
    this.setState( {
        activeForm: activeForm    
    });
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
          id="yarn-weight" value="yarn-dropdown" 
          onClick={this.handleClick}
        >
        Yarn Weight!
        </button>
        <button 
          id="yarn-brand" value="yarn-brand" 
          onClick={this.handleClick}>
        Yarn Brand!
        </button>
        <button 
          id ="patt-type-button" value="pattern-dropdown"
          onClick={this.handleClick}
        >
        Item!
        </button>
        <button 
          id="search-w-both" value="both"
          onClick={this.handleClick}
        >
        Both!
        </button>
        <form action="/search-data" id="search-patterns" 
          hidden={this.state.activeForm === "" || this.state.activeForm === "yarn-brand"}>
          <div
            id="yarn-dropdown"
            hidden={this.state.activeForm === 'pattern-dropdown'}
          >
            <h2 className="yarn">What kind of yarn do you want to use?</h2>
            <select name="yarn" className="yarn">
                <option value="">Yarn</option>
                {yarnOptions}
            </select>
          </div>
          <div 
            id="pattern_dropdown"
            hidden={this.state.activeForm === 'yarn-dropdown'} 
          >
            <h2 className="pattern_type">What kind of item do you want to make?</h2>
            <select name="pattern_type" className="pattern_type">
                <option value="">Item</option>
                {patternOptions}
            </select>
          </div>

          <input type="submit"/>
        </form>
        <form action="/search-projects" id="search-projects"
          hidden={this.state.activeForm !== 'yarn-brand'}>
          <div
            id="yarn-brand"
            hidden={this.state.activeForm !== 'yarn-brand'}
          >
            <h2 className="yarn">What brand of yarn do you want to use?</h2><br/>
            <input name="yarn-brand" type="text" className="yarn-brand typeahead"/>
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

