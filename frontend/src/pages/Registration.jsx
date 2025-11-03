import React, {useState} from 'react';
import { useNavigate } from 'react-router-dom';
import { Link } from "react-router-dom";
import styles from '../styles/Login.module.css'
import regStyles from '../styles/Registration.module.css'

export default function Registration(){
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

        <div className={styles.loginContainer}>
            <h1>Registracija</h1>
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

                    <div className={regStyles.passwordInput}>
                        <div className={styles.formGroup}>
                            <label>Lozinka</label>
                            <input type='password' placeholder='••••••••' />
                        </div>

                        <div className={styles.formGroup}>
                            <label>Ponovi lozinku</label>
                            <input type='password' placeholder='••••••••' />
                        </div>
                    </div>

                    {error && <p className={styles.error}>{error}</p>}

                    <button type='submit' className={styles.loginButton}>
                        Registriraj se
                    </button>
                </form>
            </div>
        </div>
    );
}