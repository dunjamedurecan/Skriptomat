import React from 'react'
import './login.css'

//.login-container h1: <h1>Skriptomat</h1>, u slučaju vracanja ovoga, smjestiti u .login-container na vrh


function Login() {
    return (
        <div className='login-container'>
            <div class="hover-underline">Skriptomat</div>
            <div className='login-box'>

                <form className='login-form'>
                    <div className='form-group'>
                        <label>Email</label>
                        <input type='email' placeholder='example@fer.hr' />
                    </div>
                    
                    <div className='form-group'>
                        <label>Lozinka</label>
                        <input type='password' placeholder='••••••••' />
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
                    <p>Nemaš račun? <a href='#'>Registriraj se</a></p>
                </div>
            </div>
        </div>
    )
}

export default Login
