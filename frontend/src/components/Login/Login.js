import React from 'react';

import Header from '../Header';
import Footer from '../Footer';

import '../App/App.css';
import './Login.css';

export default function Login() {
    return(
        <div className="login-wrapper">
            <Header />
            <form>
                <h2>Login Form</h2>
                <div>
                    <label>Username:</label>
                    <input type="text" />
                </div>
                <div>
                    <label>Password:</label>
                    <input type="password" />
                </div>
                <div>
                    <input type="checkbox" value="1" id="field_remember_me" />
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