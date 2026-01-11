import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import styles from '../styles/UserProfile.module.css';
import commonStyles from '../styles/Home.module.css';
import { useAuth } from '../context/AuthContext'; // Povezivanje sa kontekstom za autentifikaciju
import { documentsAPI, userAPI } from '../api/auth'; // Fetch za korisničke objave
import feedstyles from '../styles/Feed.module.css';

export default function UserProfile() {
  const { user, logout } = useAuth(); // Dohvatanje korisničkih podataka i funkcije za odjavu
  const [posts, setPosts] = useState([]); // Stanje za prikaz objava
  const [loading, setLoading] = useState(true); // Prikaz učitavanja
  const [paypalEmail, setPaypalEmail] = useState(''); // PayPal email za donacije
  const [paypalSaving, setPaypalSaving] = useState(false);
  const [paypalMessage, setPaypalMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    fetchUserPosts(); // Povlačenje korisničkih objava prilikom učitavanja
    fetchUserProfile(); // Dohvati profil za PayPal email
  }, []);

  const fetchUserProfile = async () => {
    try {
      const profile = await userAPI.getMe();
      setPaypalEmail(profile.paypal_email || '');
    } catch (err) {
      console.error('Greška pri dohvaćanju profila:', err);
    }
  };

  const fetchUserPosts = async () => {
    try {
      const data = await documentsAPI.getAll(); // Povlačenje svih objava
      const userPosts = data.filter((post) => post.user?.username === user.username || post.user === user.username); // Filtriranje po korisničkom imenu
      setPosts(userPosts); // Postavljanje u stanje
    } catch (err) {
      console.error('Greška pri dohvaćanju objava:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePaypalSave = async (e) => {
    e.preventDefault();
    setPaypalSaving(true);
    setPaypalMessage({ type: '', text: '' });
    
    try {
      await userAPI.updateMe({ paypal_email: paypalEmail || null });
      setPaypalMessage({ type: 'success', text: 'PayPal email uspješno spremljen!' });
    } catch (err) {
      console.error('Greška pri spremanju PayPal emaila:', err);
      setPaypalMessage({ type: 'error', text: 'Greška pri spremanju. Pokušajte ponovo.' });
    } finally {
      setPaypalSaving(false);
    }
  };

  return (
    <div className={commonStyles.container}>
      <header>
        <h1>Moj profil</h1>
        <nav className={commonStyles.navbar}>
          <button onClick={logout}>Odjavi se</button>
          <button>
            <Link to="/feed">Feed</Link>
          </button>
        </nav>
      </header>
      <main className={styles.profilePage}>
        {/* Sekcija sa korisničkim detaljima */}
        <div className={styles.profileDetails}>
          <h2>Korisničko ime: {user.username}</h2>
          <p>Email: {user.email}</p>
          <p>Broj objava: {posts.length}</p>
          
          {/* PayPal Email Settings */}
          <div className={styles.paypalSection}>
            <h3>☕ Donacije postavke</h3>
            <p className={styles.paypalInfo}>
              Dodaj svoj PayPal email da primaš donacije na svojim objavama.
            </p>
            <form onSubmit={handlePaypalSave} className={styles.paypalForm}>
              <input
                type="email"
                placeholder="tvoj@paypal-email.com"
                value={paypalEmail}
                onChange={(e) => setPaypalEmail(e.target.value)}
                className={styles.paypalInput}
              />
              <button 
                type="submit" 
                disabled={paypalSaving}
                className={styles.paypalButton}
              >
                {paypalSaving ? 'Spremanje...' : 'Spremi'}
              </button>
            </form>
            {paypalMessage.text && (
              <p className={`${styles.paypalMessage} ${styles[paypalMessage.type]}`}>
                {paypalMessage.text}
              </p>
            )}
          </div>
        </div>

        {/* Sekcija sa korisničkim objavama */}
        <div className={styles.profilePosts}>
          <h2>Moje objave</h2>
          {loading ? (
            <p>Učitavanje objava...</p>
          ) : posts.length === 0 ? (
            <p>Nemate objava.</p>
          ) : (
            posts.map((post) => (
              <div key={post.id} className={styles.postItem}>
                <h3>{post.title}</h3>
                <p>{post.post}</p>
                {post.file && (
                  <p>
                    <a href={post.file} target="_blank" rel="noreferrer">
                      Preuzmi PDF
                    </a>
                  </p>
                )}
              </div>
            ))
          )}
        </div>
      </main>
    </div>
  );
}
