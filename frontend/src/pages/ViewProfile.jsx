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
    const [posts, setPosts] = useState([]); 

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

  useEffect(()=>{
    if(!user)return;
    fetchUserPosts(); 
  },[user]);

   const fetchUserPosts = async () => {
       try {
          if (!user) {
         console.warn('Korisnik nije pronađen. Preskačem dohvaćanje objava.');
         return;
       }
         console.log(user);
         const data = await documentsAPI.getAll(); // Povlačenje svih objava
         const userPosts = user
     ? data.filter((post) => post.user === user.username)
     : [];
         setPosts(userPosts); // Postavljanje u stanje
       } catch (err) {
         console.error('Greška pri dohvaćanju objava:', err);
       } finally {
         setLoading(false);
       }
     };

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
             <p>Broj objava: {posts.length}</p>
           </div>
   
           {/* Sekcija sa korisničkim objavama */}
           <div className={styles.profilePosts}>
             <h2>Objave:</h2>
             {loading ? (
               <p>Učitavanje objava...</p>
             ) : posts.length === 0 ? (
               <p>Korisnik nema objava.</p>
             ) : (
               <div className={feedstyles.postsList}>
               {posts.map((post) => (
                 <div key={post.id} className={feedstyles.postItem}>
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
               ))}
               </div>
             )}
           </div>
         </main>
       </div>
     );
}