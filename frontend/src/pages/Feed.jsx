import React, { useEffect, useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import styles from '../styles/Feed.module.css';
import commonStyles from '../styles/Home.module.css';
import { useAuth } from '../context/AuthContext';
import { documentsAPI,documentFeedAPI } from '../api/auth';
import ProfileHover from './ProfileHover';
import BuyMeACoffee from '../components/BuyMeACoffee';
import {FaHeart,FaRegHeart} from 'react-icons/fa';

//dodaj odobravanje objava za moderatora

//const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

export default function Feed() {

  const { user, logout } = useAuth();

  const [posts, setPosts] = useState([]);
  const [newPost, setNewPost] = useState('');
  const [showModal, setShowModal] = useState(false);

  // PDF-upload
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState('');
  const [course, setCourse] = useState('');
  const [message, setMessage] = useState('');
  const [uploading, setUploading] = useState(false);

  const fileInputRef = useRef(null);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const data = await documentFeedAPI.getAll();
      const sortedPosts=data.sort((a,b)=>b.total_likes - a.total_likes);
      console.log("Api response",data); //prilikom učitavanja objave se sortiraju po broju lajkova
      setPosts(sortedPosts);
    } catch (err) {
      console.error('fetchPosts error', err);
      
      if (err.response?.status === 401){
        setMessage('Sesija istekla. Molimo prijavite se ponovno.');
        logout();
      } else {
        setMessage('Greška pri dohvaćanju objava.');
      }
    }
  };

  const handleLike = async (id)=>{
    try{
      const response=await documentsAPI.like(id);
      const updatedPosts=posts.map((post)=>
        post.id===id ? {...post,total_likes:response.total_likes,liked:response.liked}:post
      );
  //sortiranje nakon promjene broja lajkova (da se ne mora ponovno refreshat stranica)
      const sortedPosts=updatedPosts.sort((a,b)=>b.total_likes-a.total_likes);
      setPosts(sortedPosts);
    }catch(err){
      console.error('handleLike error',err);
    }
  };

  function onFileChange(e) {
    const f = e.target.files[0];
    if (!f) {
      setFile(null);
      return;
    }
    if (f.type !== 'application/pdf') {
      setMessage('Izaberi PDF fajl.');
      e.target.value = '';
      setFile(null);
      return;
    }
    const maxSize = 5 * 1024 * 1024; // 5 MB limit
    if (f.size > maxSize) {
      setMessage('Fajl je prevelik (max 5 MB).');
      e.target.value = '';
      setFile(null);
      return;
    }
    setMessage('');
    setFile(f);
  }

  const handleAddPost = async (e) => {
    e.preventDefault();

    if (newPost.trim() === '' && !file) {
      return alert('Unesi sadržaj objave ili priloži PDF.');
    }

    const formData = new FormData();
    formData.append('post', newPost);
    if (title.trim()) formData.append('title', title);
    if (file) formData.append('file', file, file.name);
    if (course.trim()) formData.append('course', course);
    try {
      setUploading(true);
      setMessage('');

      // Use documentsAPI instead of fetch
      const savedPost = await documentsAPI.upload(formData);
      
      // Success - update posts list
      setPosts((prev) => [savedPost, ...prev]);
      setNewPost('');
      setTitle('');
      setCourse('');
      setFile(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
      setShowModal(false);
      setMessage('Objava uspješno dodana!');
      
    } catch (err) {
      console.error('handleAddPost error', err);
      
      // Handle errors
      if (err.response?.status === 401) {
        setMessage('Sesija istekla. Molimo prijavite se ponovno.');
        logout();
      } else if (err.response?.data?.detail) {
        setMessage(err.response.data.detail);
      } else {
        setMessage('Greška pri dodavanju objave.');
      }
    } finally {
      setUploading(false);
    }
  };

  const handleApprove=async(id)=>{
    try{
      const response=await documentFeedAPI.approve(id);
      setMessage('Objava odobrena.');
      setPosts(posts.filter((post)=>post.id!==id));
    } catch(err){
      console.error('handleApprove error', err);
      setMessage('Greška pri odobravanju objave.');
    }
  };

  const handleDecline=async(id)=>{
    try{
      const response=await documentFeedAPI.decline(id);
      setMessage('Objava odbijena.');
      setPosts(posts.filter((post)=>post.id!==id));
    } catch(err){
      console.error('handleDecline error', err);
      setMessage('Greška pri odbijanju objave.');
    }
  };

  return (
    <div className={commonStyles.container}>
      <header>
        <h1>Skriptomat</h1>
        <nav className={commonStyles.navbar}>
          <button onClick={logout}>Odjavi se</button>
          <button><Link to="/my-profile">Profil</Link></button>
        </nav>
      </header>

      <main className={styles.feedMain}>
        <div className={styles.feedCard}>
          <button className={styles.openModalBtn} onClick={() => setShowModal(true)}>Nova objava</button>

          {showModal && (
            <div className={styles.modalOverlay} onClick={() => setShowModal(false)}>
              <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
                <h3>Napiši novu objavu</h3>
                <form className={styles.newPostForm} onSubmit={handleAddPost}>
                  <textarea
                    value={newPost}
                    onChange={(e) => setNewPost(e.target.value)}
                    placeholder="Unesi sadržaj objave..."
                  ></textarea>

                  <hr />
                  
                  <textarea 
                    value={title} 
                    onChange={(e)=>setTitle(e.target.value)}
                    placeholder='Unesi naslov dokumenta'
                  ></textarea>

                  <textarea value={course} onChange={(e)=>setCourse(e.target.value)} placeholder='Unesi kolegij'></textarea>
                  
                  <h4>Priloži PDF</h4>

                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="application/pdf"
                    onChange={onFileChange}
                  />

                  {file && (
                    <div style={{padding: '0.75rem', background: 'rgba(99, 102, 241, 0.1)', border: '1px solid rgba(99, 102, 241, 0.3)', borderRadius: '8px', color: '#d1d5db', fontSize: '0.9rem'}}>
                      <small>Priloženo: {file.name} ({Math.round(file.size / 1024)} KB)</small>
                    </div>
                  )}

                  <button type="submit" disabled={uploading}>
                    {uploading ? 'Spremanje...' : 'Objavi'}
                  </button>
                  
                  <button type="button" className={styles.closeModalBtn} onClick={() => setShowModal(false)}>
                    Zatvori
                  </button>

                  {message && <p className={styles.message}>{message}</p>}
                </form>
              </div>
            </div>
          )}

          <div className={styles.postsList}>
            {posts.length === 0 ? (
              <p className={styles.noPosts}>Još nema objava.</p>
            ) : (
              posts.map((post) => (
                <div key={post.id} className={styles.postItem}>
                  <p><ProfileHover user={post.user || 'Nepoznato'} /></p>
                  <span className={styles.postDate}>{post.uploaded_at || post.date}</span>
                  <p>{post.title}</p>
                  <p>{post.post}</p>
                  
                  {post.file && (
                    <p>
                      <a href={post.file} target="_blank" rel="noreferrer">Preuzmi PDF</a>
                    </p>
                  )}
                  
                  <div className={styles.postActions}>
                    {user.role==='student' ? (<button onClick={()=>handleLike(post.id)} className={post.liked ? styles.likedBtn : styles.likeBtn}>
                      {post.liked ? (<FaHeart className={styles.iconFilled} />) : (<FaRegHeart className={styles.iconOutlined} />)}
                      <p>{post.total_likes}</p>
                    </button>):(
                      <><button className={styles.openModalBtn} onClick={()=>handleApprove(post.id)}>Odobri</button>
                    <button className={styles.openModalBtn} onClick={()=>handleDecline(post.id)}>Odbij</button></>)
                    }
                    
                    
                    {/* Buy Me a Coffee button - only shows if author has PayPal email */}
                    <BuyMeACoffee 
                      authorPaypalEmail={post.user?.paypal_email}
                      authorName={post.user?.username || post.user?.first_name || 'autora'}
                      postTitle={post.title}
                    />
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </main>
    </div>
  );
}