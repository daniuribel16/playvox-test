import React, { Component } from 'react';
import './App.css';
import Users from './components/users';
import 'bootstrap/dist/css/bootstrap.css';

export class App extends Component {
  render = () => {
    return (
      <div className="container-fluid">
        <Users />
      </div>
    );
  }
}

export default App;
