import React, {useState,useEffect} from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI } from '../api/auth';
import styles from '../styles/Login.module.css';
import regStyles from '../styles/Registration.module.css';

export default function Registration(){
    const [formData, setFormData] = useState({
        email: '',
        username: '',
        password: '',
        password_confirm: '',
        first_name: '',
        last_name: '',
        role: '',
        faculty: ''
    });
    
    // UI state
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();
    const [step, setStep]=useState(1);
    const[usinggoogle,setUsingGoogle]=useState(false);
    const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;

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
        

        if (!formData.username) {
            setError('Korisničko ime je obavezno');
            return;
        }

        

        // Call backend
        setLoading(true);
        try {
            console.log("Podaci za registraciju:", formData);
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
                console.log("Greška kod registracije:",err.response.data);
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
    async function handleFirstStep(e){
        e.preventDefault();
        setError('');

        if (!validateEmail(formData.email)) {
            setError('Upiši ispravnu email adresu');
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
        setStep(2);
    }

    async function handleSecondStep(e){
        e.preventDefault();
        setError('');
        setLoading(true);
        
        try {
             console.log("Podaci za registraciju:", formData);
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
                 console.log("Greška kod registracije:",err.response.data);
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
    useEffect(() => {
            if (!GOOGLE_CLIENT_ID) {
                console.warn('VITE_GOOGLE_CLIENT_ID not set');
                return;
            }
            
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
        }, [GOOGLE_CLIENT_ID])
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
                    const data = await authAPI.googleRegister({ id_token });
                    console.log('Google registration successful:', data);
                    console.log(data.email);
                    setFormData({
                        ...formData,
                        email:data.email,
                    });
                    console.log("Postavljeni podaci nakon Google registracije,:",formData);
                    setStep(2);
                    setUsingGoogle(true);
                } catch (err) {
                    console.error('Google login error:', err);
                    setError(err.response?.data?.error || 'Greška pri Google prijavi');
                } finally {
                    setLoading(false);
                }
            }
    return(

        <div className={styles.loginContainer}>
            <h1>Registracija</h1>
            <div className={regStyles.registrationBox}>
                {step===1 ? (
                    //Prvi korak - unos emaila i lozinke
                    <form onSubmit={handleFirstStep} className={styles.loginForm}>
                        <div className={styles.inputRow}>
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
                             <div style={{ marginTop: 16, display: 'flex', justifyContent: 'center' }}>
                            {/* Google button will be rendered here by Google's script */}
                    <div id="googleSignInDiv"></div>
                </div>
                        </div>
                        {error && <p className={styles.error}>{error}</p>}
                        <button type="submit" className={styles.loginButton} disabled={loading}>{loading ? "Registracija..." : "Dalje"}</button>
                    </form>
                ):(
                    //Drugi korak - korisničko ime, vrsta user-a, unos fakulteta...
                    <form onSubmit={handleSecondStep} className={styles.loginForm}>
                        <div className={regStyles.inputRow}>
                            <div className={regStyles.formGroup}>
                                <label>Korisničko ime</label>
                                <input
                                    type="text"
                                    name="username"
                                    value={formData.username}
                                    onChange={handleChange}
                                    placeholder='korisnik123'
                                    required
                                />
                            </div>
                        </div>
                        {usinggoogle ? (<div className={regStyles.inputRow}>
                            <div className={styles.formGroup}>
                                <label>Lozinka za prijavu putem maila</label>
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
                        </div>):null}
                        <div className={regStyles.inputRow}>
                        <div className={regStyles.formGroup}>
                            <label>Ime (opcionalno)</label>
                            <input
                                type='text'
                                name='first_name'
                                value={formData.first_name}
                                onChange={handleChange}
                                placeholder='Ime'
                            />
                        </div>

                        <div className={regStyles.formGroup}>
                            <label>Prezime (opcionalno)</label>
                            <input
                                type='text'
                                name='last_name'
                                value={formData.last_name}
                                onChange={handleChange}
                                placeholder='Prezime'
                            />
                        </div>
                    </div>
                    <div className={regStyles.inputRow}>
                        <div className={regStyles.formGroup}>
                            <label>Oblik korisnika</label>
                            <select
                                name="role"
                                value={formData.role}
                                onChange={handleChange}
                                required
                            >
                                <option value="">Odaberi oblik korisnika</option>
                                <option value="student">Student</option>
                                <option value="moderator">Moderator</option>
                            </select>
                        </div>
                        <div className={regStyles.formGroup}>
                            <label>Fakultet</label>
                            <input
                                type="text"
                                name="faculty"
                                value={formData.faculty}
                                onChange={handleChange}
                                placeholder="Npr. Fakultet elektrotehnike i računarstva"
                                required
                            />
                        </div>
                    </div>
                    {error && <p className={styles.error}>{error}</p>}
                    <button type="submit" className={styles.loginButton} disabled={loading}>{loading ? "Završi registraciju..." : "Registriraj se"}</button>
                    </form>
                )}
            </div>
        </div>
    );
}