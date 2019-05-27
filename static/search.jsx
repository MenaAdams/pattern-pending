
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
          name="yarn-search" id="yarn-search" value="yarn-dropdown" 
          onClick={this.handleClick}
        >
        Yarn Weight!
        </button>
        <button 
          name="patt-type-button" id ="patt-type-button" value="pattern-dropdown"
          onClick={this.handleClick}
        >
        Category!
        </button>
        <button 
          name="search_w_both" id="search_w_both" value="both"
          onClick={this.handleClick}
        >
        Both!
        </button>
        <form action="/search-data" id="search-form" hidden={this.state.activeForm === ""}>
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
                <option value="">Category</option>
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

