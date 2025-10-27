import React, {useState} from 'react';
import { useNavigate } from 'react-router-dom';
import { Link } from "react-router-dom";

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
        <div className="login-container">
            <div className='login-card'>
            <h2>Registracija</h2>
            <form onSubmit={handleSubmit} className="login-form">
            <label>
                Email
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="ime@primjer.com" required/>
            </label>
            {error && <div className="error">{error}</div>}
            <button type="submit">Prijavi se</button>
            <p>Imaš račun,<Link to="/login">prijavi se</Link> </p>
            </form>
            </div>
        </div>
    );
}