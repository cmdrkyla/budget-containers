import React, { useState } from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom';

import Header from '../Header';
import Footer from '../Footer';
import Login from '../Login/Login';
import Dashboard from '../Dashboard/Dashboard';

import './App.css';

function App() {
  const [token, setToken] = useState();

  if(!token) {
    return <Login setToken={setToken} />
  }
  
  return (
    <div className="App">
      <Header />
      <div className="App-content">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Dashboard />} />
          </Routes>
        </BrowserRouter>
      </div>
      <Footer />
    </div>
  );
}

export default App;
