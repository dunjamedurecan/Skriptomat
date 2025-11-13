import React, {useState} from 'react';
import { useNavigate } from 'react-router-dom';
import { Link } from "react-router-dom";
import styles from '../styles/Login.module.css';
import regStyles from '../styles/Registration.module.css';

export default function Registration(){
    const [formData, setFormData] = useState({
        email: '',
        username: '',
        password: '',
        password_confirm: '',
        first_name: '',
        last_name: ''
    });
    
    // UI state
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    // Email validation
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // Handle input changes
    function handleChange(e) {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    }

    // Handle form submission
    async function handleSubmit(e) {
        e.preventDefault();
        setError('');

        // Validation
        if (!validateEmail(formData.email)) {
            setError('Upiši ispravnu email adresu');
            return;
        }

        if (!formData.username) {
            setError('Korisničko ime je obavezno');
            return;
        }

        if (formData.password.length < 8) {
            setError('Lozinka mora imati minimalno 8 znakova');
            return;
        }

        if (formData.password !== formData.password_confirm) {
            setError('Lozinke se ne podudaraju');
            return;
        }

        // Call backend
        setLoading(true);
        try {
            const response = await authAPI.register(formData);
            console.log('Registration successful:', response);
            
            // Show success message and redirect
            alert('Registracija uspješna! Molimo prijavite se.');
            navigate('/login');
            
        } catch (err) {
            console.error('Registration error:', err);
            
            // Handle different error types
            if (err.response?.data) {
                // Backend validation errors
                const errors = err.response.data;
                if (errors.email) {
                    setError(errors.email[0]);
                } else if (errors.username) {
                    setError(errors.username[0]);
                } else if (errors.password) {
                    setError(errors.password[0]);
                } else {
                    setError('Greška pri registraciji. Pokušaj ponovno.');
                }
            } else {
                setError('Greška pri povezivanju sa serverom');
            }
        } finally {
            setLoading(false);
        }
    }

    return(

        <div className={styles.loginContainer}>
            <h1>Registracija</h1>
            <div className={styles.loginBox}>
                <form onSubmit={handleSubmit} className={styles.loginForm}>
                    
                    {/* Email */}
                    <div className={styles.formGroup}>
                        <label>Email</label>
                        <input
                            type='email'
                            name='email'
                            value={formData.email}
                            onChange={handleChange}
                            placeholder='example@fer.hr'
                            required
                        />
                    </div>

                    {/* Username */}
                    <div className={styles.formGroup}>
                        <label>Korisničko ime</label>
                        <input
                            type='text'
                            name='username'
                            value={formData.username}
                            onChange={handleChange}
                            placeholder='korisnik123'
                            required
                        />
                    </div>

                    {/* First Name (Optional) */}
                    <div className={styles.formGroup}>
                        <label>Ime (opcionalno)</label>
                        <input
                            type='text'
                            name='first_name'
                            value={formData.first_name}
                            onChange={handleChange}
                            placeholder='Ime'
                        />
                    </div>

                    {/* Last Name (Optional) */}
                    <div className={styles.formGroup}>
                        <label>Prezime (opcionalno)</label>
                        <input
                            type='text'
                            name='last_name'
                            value={formData.last_name}
                            onChange={handleChange}
                            placeholder='Prezime'
                        />
                    </div>

                    {/* Passwords */}
                    <div className={regStyles.passwordInput}>
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

                        <div className={styles.formGroup}>
                            <label>Ponovi lozinku</label>
                            <input
                                type='password'
                                name='password_confirm'
                                value={formData.password_confirm}
                                onChange={handleChange}
                                placeholder='••••••••'
                                required
                            />
                        </div>
                    </div>

                    {/* Error message */}
                    {error && <p className={styles.error}>{error}</p>}

                    {/* Submit button */}
                    <button
                        type='submit'
                        className={styles.loginButton}
                        disabled={loading}
                    >
                        {loading ? 'Registracija...' : 'Registriraj se'}
                    </button>

                    {/* Link to login */}
                    <p style={{ marginTop: '1rem', textAlign: 'center' }}>
                        Već imaš račun? <Link to="/login">Prijavi se</Link>
                    </p>
                </form>
            </div>
        </div>
    );
}