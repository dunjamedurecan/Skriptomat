import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import styles from '../styles/UserProfile.module.css';
import commonStyles from '../styles/Home.module.css';
import { useAuth } from '../context/AuthContext'; // Povezivanje sa kontekstom za autentifikaciju
import { documentsAPI } from '../api/auth'; // Fetch za korisničke objave
import feedstyles from '../styles/Feed.module.css';

export default function UserProfile() {
  const { user, logout } = useAuth(); // Dohvatanje korisničkih podataka i funkcije za odjavu
  const [posts, setPosts] = useState([]); // Stanje za prikaz objava
  const [loading, setLoading] = useState(true); // Prikaz učitavanja 

  useEffect(() => {
    fetchUserPosts(); // Povlačenje korisničkih objava prilikom učitavanja
  }, []);

  const fetchUserPosts = async () => {
    try {
      const data = await documentsAPI.getAll(); // Povlačenje svih objava
      const userPosts = data.filter((post) => post.user === user.username); // Filtriranje po korisničkom imenu
      setPosts(userPosts); // Postavljanje u stanje
    } catch (err) {
      console.error('Greška pri dohvaćanju objava:', err);
    } finally {
      setLoading(false);
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
