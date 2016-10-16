import React, { Component } from 'react';
import logo from './logo.svg';
import load from './load.gif';
import './App.css';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      loading: false,
      content: "",
    };
  }
  onChange(e) {
    this.setState({
      loading: false,
      content: e.target.value,
    });
  }
  onSubmit(e) {
    let text = this.state.content;
    this.setState({
      loading: true,
      content: text,
    });
    console.info(text);

    fetch('/translate', {
             method: 'POST',
             headers: {
               'Accept': 'application/json',
               'Content-Type': 'application/json'
             },
             body: JSON.stringify({
               text,
             })
           })
           .then(res => {
             return res.json();
           })
           .then(data => {
              this.setState({
                loading: false,
                content: data.text,
              });
           });
  }
  render() {
    let loading = this.state.loading;
    let spin = null;
    if (loading) {
      spin = (<img src={load} />);
    }
    let onSubmit = this.onSubmit.bind(this);
    let onChange = this.onChange.bind(this);
    return (
     <div>
     <div className="jumbotron secondd"> 
        <h2 className="hi"><span className="glyphicon glyphicon-pencil" aria-hidden="true"></span>  Decomplicate </h2>
        <div className="text">
          <form>
            <div>
              <textarea id="text-body" name="d" placeholder="Paste your text here!" value={this.state.content} onChange={onChange} disabled={loading} />
            </div>
            <button className="btn btn-primary btn-lg" disabled={loading} onClick={onSubmit}>Turn it in</button>
            <div class='spinner'>
            {spin}
            </div>
          </form>
       </div>
     </div>
    </div>
    );
  }
}

export default App;
