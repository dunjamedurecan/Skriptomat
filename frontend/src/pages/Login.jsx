import React, {useState, useEffect} from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {authAPI} from '../api/auth';
import styles from '../styles/Login.module.css';
import { useAuth } from '../context/AuthContext';


export default function Login(){
    
    const { login } = useAuth();
    
    const { isAuthenticated } = useAuth();
    const [formData, setFormData] = useState({
        username: '', // email or username
        password: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    
    const navigate=useNavigate();
    // This is so that logged in users cannot get back into Login
    useEffect(() => {
        if (isAuthenticated) {
            navigate('/feed');
        }
    }, [isAuthenticated, navigate]);

    function handleChange(e){
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    }

    async function handleSubmit(e) {
        e.preventDefault();
        setError('');

        // Validation
        if (!formData.username) {
            setError('Upiši email ili korisničko ime');
            return;
        }

        if (!formData.password) {
            setError('Upiši lozinku');
            return;
        }

        // Call backend
        setLoading(true);
        try {
            const response = await authAPI.login(formData);
            console.log('Login successful:', response);

            // Store tokens in localStorage
            login(
                {
                    access_token: response.access_token,
                    refresh_token: response.refresh_token
                },
                response.user
            );

            // Redirect to feed
            navigate('/feed');

        } catch (err) {
            console.error('Login error:', err);

            if (err.response?.status === 401) {
                setError('Pogrešno korisničko ime ili lozinka');
            } else if (err.response?.status === 403) {
                setError('Račun je onemogućen');
            } else if (err.response?.data?.error) {
                setError(err.response.data.error);
            } else {
                setError('Greška pri povezivanju sa serverom');
            }
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className={styles.loginContainer}>
            <h1>Skriptomat</h1>
            <div className={styles.loginBox}>
                <form onSubmit={handleSubmit} className={styles.loginForm}>
                    <div className={styles.formGroup}>
                        <label>Email ili Korisničko ime</label>
                        <input 
                            type='text'
                            name='username' 
                            value={formData.username}
                            onChange={handleChange}
                            placeholder='example@fer.hr ili korisnik123'
                            required
                        />
                    </div>

                    <div className={styles.formGroup}>
                        <label>Lozinka</label>
                        <input
                            type='password'
                            name='password'
                            value={formData.password}
                            onChange={handleChange}
                            placeholder='••••••••'
                            required
                        />
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

                    <button
                        type='submit'
                        className={styles.loginButton}
                        disabled={loading}
                    >
                        {loading ? 'Prijava...' : 'Prijavi se'}
                    </button>

                </form>

                <div className={styles.registerLink}>
                    <p>Nemaš račun? <Link to="/registration">Registriraj se</Link></p>
                </div>
            </div>
        </div>
    );
}