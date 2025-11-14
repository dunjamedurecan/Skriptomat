import React, {useState, useEffect} from 'react';
import { useNavigate, Link } from 'react-router-dom';
import authAPI from '../api/auth';
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

  const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;
    // This is so that logged in users cannot get back into Login
    useEffect(() => {
        if (isAuthenticated) {
            navigate('/feed');
        }
    }, [isAuthenticated, navigate]);

     useEffect(() => {
        if (!GOOGLE_CLIENT_ID) {
            console.warn('VITE_GOOGLE_CLIENT_ID / REACT_APP_GOOGLE_CLIENT_ID not set');
            return;
        }
       console.log('authAPI object:', authAPI);
    console.log('authAPI.google typeof:', typeof authAPI?.google);
    console.log('window.location.origin:', window.location.origin);
        // avoid loading twice
        if (document.getElementById('google-client-script')) return;

        const script = document.createElement('script');
        script.src = 'https://accounts.google.com/gsi/client';
        script.async = true;
        script.defer = true;
        script.id = 'google-client-script';
        script.onload = () => {
            if (window.google && window.google.accounts && window.google.accounts.id) {
                window.google.accounts.id.initialize({
                    client_id: GOOGLE_CLIENT_ID,
                    callback: handleCredentialResponse,
                    ux_mode: 'popup' // popup is friendlier for SPA
                });

                // render button inside container
                const container = document.getElementById('googleSignInDiv');
                if (container) {
                    window.google.accounts.id.renderButton(container, {
                        theme: 'outline',
                        size: 'large',
                        text: 'signin_with'
                    });
                }
            }
        };
        document.body.appendChild(script);
    })
    async function handleCredentialResponse(response) {
        setError('');
        setLoading(true);

        const id_token = response?.credential;
        if (!id_token) {
            setError('Google login nije uspio (nema tokena).');
            setLoading(false);
            return;
        }

        try {
            // send id_token to your backend endpoint
            const data = await authAPI.google({ id_token });
            // data should contain access_token, refresh_token, user
            login(
                {
                    access_token: data.access_token,
                    refresh_token: data.refresh_token
                },
                data.user
            );
            navigate('/feed');
        } catch (err) {
            console.error('Google login error:', err);
            setError(err.response?.data?.error || 'Greška pri Google prijavi');
        } finally {
            setLoading(false);
        }
    }
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
                    <div style={{ marginTop: 16, display: 'flex', justifyContent: 'center' }}>
                    {/* Google button will be rendered here by Google's script */}
                    <div id="googleSignInDiv"></div>
                </div>
                <div className={styles.registerLink}>
                    <p>Nemaš račun? <Link to="/registration">Registriraj se</Link></p>
                </div>
            </div>
        </div>
    );
}