import React, { useEffect, useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import styles from '../styles/Feed.module.css';
import commonStyles from '../styles/Home.module.css';
import { useAuth } from '../context/AuthContext';
import { documentsAPI } from '../api/auth';

export default function UserProfile(){
    return(<div className={commonStyles.container}>
          <header>
            <h1>Moj profil</h1>
            <nav className={commonStyles.navbar}>
              <button >Odjavi se</button>
              <button><Link to="/feed">Feed</Link></button>
            </nav>
          </header>
          </div>);

}