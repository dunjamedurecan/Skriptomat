import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import styles from '../styles/UserProfile.module.css';
import commonStyles from '../styles/Home.module.css';
import { useAuth } from '../context/AuthContext'; // Povezivanje sa kontekstom za autentifikaciju
import { documentsAPI } from '../api/auth'; // Fetch za korisničke objave
import feedstyles from '../styles/Feed.module.css';
import { useParams } from 'react-router-dom';
import { getUserProfile } from '../api/client';

export default function ViewProfile() {
    const {username}=useParams();
    const [user,setUser]=useState(null);
    const [loading, setLoading]=useState(true);

    useEffect(() => {
    const fetchUserProfile = async () => {
      try {
        const data = await getUserProfile(username); // API poziv za korisnika
        setUser(data);
      } catch (err) {
        console.error("Greška pri dohvaćanju korisničkog profila:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchUserProfile();
  }, [username]);

  if (loading) {
    return <p>Učitavanje korisničkih podataka...</p>;
  }

  if (!user) {
    return <p>Korisnik nije pronađen.</p>;
  }

  return (
    <div className={commonStyles.container}>
          <header>
            <h1>{user.username}</h1>
            <nav className={commonStyles.navbar}>
             
              <button>
                <Link to="/feed">Feed</Link>
              </button>
            </nav>
          </header>
          <main className={styles.profilePage}>
            {/* Sekcija sa korisničkim detaljima */}
            <div className={styles.profileDetails}>
              <h2>Korisnik: {user.first_name} {user.last_name}</h2>
              <p>Email: {user.email}</p>
              <p>Tip korisnika: {user.role}</p>
              <p>Fakultet: {user.faculty}</p>
            </div>
            </main>
           </div>
  );
}