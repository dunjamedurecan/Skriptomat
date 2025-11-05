import React, {useState} from 'react';
import { useNavigate, Link } from 'react-router-dom';
import styles from '../styles/Login.module.css';

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

    return (
        <div className={styles.loginContainer}>
            <h1>Skriptomat</h1>
            <div className={styles.loginBox}>
                <form onSubmit={handleSubmit} className={styles.loginForm}>
                    <div className={styles.formGroup}>
                        <label>Email or Username</label>
                        <input 
                            type='email' 
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder='example@fer.hr'
                        />
                    </div>

                    <div className={styles.formGroup}>
                        <label>Lozinka</label>
                        <input type='password' placeholder='••••••••' />
                    </div>

                    <div className={styles.formOptions}>
                        <label className={styles.rememberMe}>
                            <input type='checkbox' />
                            <span>Zapamti me</span>
                        </label>
                        <a href='#' className={styles.forgotPassword}>
                            Zaboravljena lozinka?
                        </a>
                    </div>

                    {error && <p className={styles.error}>{error}</p>}

                    <button type='submit' className={styles.loginButton}>
                        Prijavi se
                    </button>
                </form>

                <div className={styles.registerLink}>
                    <p>Nemaš račun? <Link to="/registration">Registriraj se</Link></p>
                </div>
            </div>
        </div>
    );
}