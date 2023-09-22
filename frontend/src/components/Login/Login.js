import React, {useState} from 'react';
import PropTypes from 'prop-types';

import Header from '../Header';
import Footer from '../Footer';

import '../App/App.css';
import './Login.css';

export default function Login({ setToken }) {
    const [email_address, setEmailAddress] = useState();
    const [password, setPassword] = useState();
    const [remember_me, setRememberMe] = useState();

    const handleSubmit = async e => {
        e.preventDefault();
        const token = await loginUser({
          email_address,
          password,
          remember_me
        });
        setToken(token);
      }

    return(
        <div className="login-wrapper">
            <Header />
            <form onSubmit={handleSubmit}>
                <h2>Login Form</h2>
                <div>
                    <label>Email Address:</label>
                    <input type="text" onChange={e => setEmailAddress(e.target.value)} />
                </div>
                <div>
                    <label>Password:</label>
                    <input type="password" onChange={e => setPassword(e.target.value)} />
                </div>
                <div>
                    <input type="checkbox" id="field_remember_me" onChange={e => setRememberMe(e.target.checked)} />
                    <label for="field_remember_me">Remember Me</label>
                </div>
                <div>
                    <button type="submit">Submit</button>
                </div>
            </form>
            <Footer />
        </div>
    );
}

Login.propTypes = {
    setToken: PropTypes.func.isRequired
  }


async function loginUser(credentials) {
  return fetch('http://localhost:8081/api/auth/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  }).then(response => {
    if(!response.ok)
      throw new Error(response.status);
    else
      return response.json();
  }).then((data) => {
    return data
  })
  .catch((error) => {
    /* TODO: figure out how to set an error message on the page */
    alert("There was a problem logging in")
  });
}
