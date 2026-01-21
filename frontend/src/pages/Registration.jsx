import React, {useState,useEffect} from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { authAPI, userAPI } from '../api/auth';
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
    const [googleReady, setGoogleReady] = useState(false);
    const navigate = useNavigate();
    const [step, setStep]=useState(1);
    const[usinggoogle,setUsingGoogle]=useState(false);
    const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;

    // Hardcoded faculties list
    const faculties = [
        { id: 1, name: "FER" },
        { id: 2, name: "PMF" },
        { id: 3, name: "FFSE" },
        { id: 4, name: "FSB" },
        { id: 5, name: "FFZG" },
        { id: 6, name: "Fakultet elektrotehnike i računarstva (FER)" },
        { id: 7, name: "Prirodoslovno-matematički fakultet (PMF)" },
        { id: 8, name: "Fakultet strojarstva i brodogradnje (FSB)" },
        { id: 9, name: "Ekonomski fakultet" },
        { id: 10, name: "Pravni fakultet" },
        { id: 11, name: "Filozofski fakultet" },
        { id: 12, name: "Medicinski fakultet" },
        { id: 13, name: "Građevinski fakultet" },
        { id: 14, name: "Arhitektonski fakultet" },
        { id: 15, name: "Fakultet prometnih znanosti" },
        { id: 16, name: "Fakultet kemijskog inženjerstva i tehnologije" },
        { id: 17, name: "Tekstilno-tehnološki fakultet" },
        { id: 18, name: "Metalurški fakultet" },
        { id: 19, name: "Rudarsko-geološko-naftni fakultet" },
        { id: 20, name: "Agronomski fakultet" },
        { id: 21, name: "Šumarski fakultet" },
        { id: 22, name: "Prehrambeno-biotehnološki fakultet" },
        { id: 23, name: "Veterinarski fakultet" },
        { id: 24, name: "Farmaceutsko-biokemijski fakultet" },
        { id: 25, name: "Edukacijsko-rehabilitacijski fakultet" },
        { id: 26, name: "Kineziološki fakultet" },
        { id: 27, name: "Učiteljski fakultet" },
        { id: 28, name: "Akademija likovnih umjetnosti" },
        { id: 29, name: "Glazbena akademija" },
        { id: 30, name: "Akademija dramske umjetnosti" },
    ];

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
            
            // Use different endpoint for Google users
            const response = usinggoogle 
                ? await authAPI.googleRegisterComplete(formData)
                : await authAPI.register(formData);
            
            console.log('Registration successful:', response);
            
            // If Google registration, auto-login with returned tokens
            if (usinggoogle && response.access_token) {
                localStorage.setItem('access_token', response.access_token);
                localStorage.setItem('refresh_token', response.refresh_token);
                navigate('/feed');
                return;
            }
            
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
        
        // Check if script already exists
        const existingScript = document.getElementById('google-client-script');
        
        if (existingScript) {
            // Script exists, check if Google is ready
            if (window.google?.accounts?.id) {
                initializeGoogleButton();
            } else {
                // Wait for script to load
                existingScript.addEventListener('load', initializeGoogleButton);
            }
            return;
        }

        // Create new script
        const script = document.createElement('script');
        script.src = 'https://accounts.google.com/gsi/client';
        script.async = true;
        script.defer = true;
        script.id = 'google-client-script';
        script.onload = initializeGoogleButton;
        document.body.appendChild(script);
    }, [GOOGLE_CLIENT_ID]);
    
    const initializeGoogleButton = () => {
        if (window.google?.accounts?.id) {
            window.google.accounts.id.initialize({
                client_id: GOOGLE_CLIENT_ID,
                callback: handleCredentialResponse,
                ux_mode: 'popup'
            });

            const container = document.getElementById('googleSignInDiv');
            if (container) {
                window.google.accounts.id.renderButton(container, {
                    theme: 'outline',
                    size: 'large',
                    text: 'signin_with'
                });
                setGoogleReady(true);
            }
        }
    };
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
                    
                    // Store Google data (email, names) and move to completion step
                    setFormData({
                        ...formData,
                        email: data.email,
                        first_name: data.first_name || '',
                        last_name: data.last_name || ''
                    });
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
                        {usinggoogle && (
                            <div className={regStyles.googleInfo}>
                                <p style={{color: '#10b981', fontSize: '0.9rem', marginBottom: '1rem'}}>✓ Registracija putem Google računa</p>
                            </div>
                        )}
                        <div className={regStyles.inputRow}>
                        <div className={regStyles.formGroup}>
                            <label>Ime {usinggoogle ? '(od Google - moguće promijeniti)' : '(opcionalno)'}</label>
                            <input
                                type='text'
                                name='first_name'
                                value={formData.first_name}
                                onChange={handleChange}
                                placeholder='Ime'
                            />
                        </div>

                        <div className={regStyles.formGroup}>
                            <label>Prezime {usinggoogle ? '(od Google - moguće promijeniti)' : '(opcionalno)'}</label>
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
                            <select
                                name="faculty"
                                value={formData.faculty}
                                onChange={handleChange}
                                required
                            >
                                <option value="">Odaberi fakultet</option>
                                {faculties.map((faculty) => (
                                    <option key={faculty.id} value={faculty.name}>
                                        {faculty.name}
                                    </option>
                                ))}
                            </select>
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