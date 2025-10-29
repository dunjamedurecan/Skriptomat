import React, {useState} from 'react';
import { useNavigate } from 'react-router-dom';
import { Link } from "react-router-dom";
import '../styles/login.css'

export default function Login(){
    const [email, setEmail]=useState('');
    const [error, setError]=useState('');
    const navigate=useNavigate();

    function validateEmail(email){
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    function handleSubmit(e){
        e.preventDefault();
        if(!validateEmail(email)){
            setError('Upiši ispravnu email adresu');
            return;
        }
        setError('');
        navigate('/feed');
    }

    return(
        <div className="login-container">
            <h1>Skriptomat</h1>
            <div className='login-box'>
                
                <form onSubmit={handleSubmit} className="login-form">

                    <div className='form-group'>
                        <label>Email or Username</label>
                        <input type='email' placeholder='example@fer.hr'></input>
                    </div>

                    <div className='form-group'>
                        <label>Lozinka</label>
                        <input type='password' placeholder='••••••••'></input>
                    </div>

                    <div className='form-options'>
                        <label className='remember-me'>
                            <input type='checkbox' />
                            <span>Zapamti me</span>
                        </label>
                        <a href='#' className='forgot-password'>Zaboravljena lozinka?</a>
                    </div>

                    <button type='submit' className='login-button'>Prijavi se</button>

                </form>

                <div className='register-link'>
                    <p>Nemaš račun? <a href='#' Registriraj se></a></p>
                </div>

            </div>
        </div>
    );
}