import logo from './logo.svg';
import './App.css';
import React, { Component }  from 'react';
import ForceGraph2D from './react-force-graph-2d';
import genRandomTree from './random-data';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
      <ForceGraph2D graphData={genRandomTree}/>,
    </div>
  );
}

export default App;
