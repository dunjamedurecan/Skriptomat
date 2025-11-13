import React, { useEffect, useState, useRef } from 'react';
import { Link } from 'react-router-dom';
import styles from '../styles/Feed.module.css';
import commonStyles from '../styles/Home.module.css';
import { useAuth } from '../context/AuthContext'

const API_BASE = import.meta.env.VITE_API_BASE_URL || '';

export default function Feed() {

  const { user, logout } = useAuth();

  const [posts, setPosts] = useState([]);
  const [newPost, setNewPost] = useState('');
  const [showModal, setShowModal] = useState(false);

  // PDF-upload
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState('');
  const [message, setMessage] = useState('');
  const [uploading, setUploading] = useState(false);

  const fileInputRef = useRef(null);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const res = await fetch(`${API_BASE}/api/posts/documents/`, { credentials: 'include' });
      if (!res.ok) throw new Error('Ne mogu dohvatiti objave');
      const data = await res.json();
      setPosts(data);
    } catch (err) {
      console.error('fetchPosts error', err);
      setMessage('Greška pri dohvaćanju objava.');
    }
  };

  // helper za CSRF cookie (ako koristiš Django session auth)
  function getCookie(name) {
    const match = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return match ? match.pop() : '';
  }

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

    // zahtjevamo bar tekst ili fajl
    if (newPost.trim() === '' && !file) {
      return alert('Unesi sadržaj objave ili priloži PDF.');
    }

    const formData = new FormData();
    formData.append('post', newPost);
    if (title.trim()) formData.append('title', title);
    if (file) formData.append('file', file, file.name);

    try {
      setUploading(true);
      setMessage('');
      const csrfToken = getCookie('csrftoken'); // Django CSRF cookie

      const res = await fetch(`${API_BASE}/api/posts/documents/`, {
        method: 'POST',
        body: formData,
        credentials: 'include', // važno za cookie-based auth / CSRF
        headers: csrfToken ? { 'X-CSRFToken': csrfToken } : {},
      });

      if (!res.ok) {
        const errBody = await res.json().catch(() => null);
        console.error('Upload/Save post error', errBody || res.statusText);
        setMessage(errBody?.detail || 'Greška pri spremanju objave.');
        return;
      }

      const savedPost = await res.json();
      setPosts((prev) => [savedPost, ...prev]);
      setNewPost('');
      setTitle('');
      setFile(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
      setShowModal(false);
      setMessage('Objava je uspješno spremljena.');
    } catch (err) {
      console.error('handleAddPost error', err);
      setMessage('Greška pri slanju objave.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className={commonStyles.container}>
      <header>
        <h1>Skriptomat</h1>
        <nav className={commonStyles.navbar}>
          <Link to="/">Profil</Link>
          <Link to="/">Odjava</Link>
          <button onClick={logout}>Odjavi se</button>
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
                  <textarea value={title} onChange={(e)=>setTitle(e.target.value)}
                  placeholder='Unesi naslov dokumenta'></textarea>
                  <h4>Priloži PDF </h4>

                  <input
                    ref={fileInputRef}
                    type="file"
                    accept="application/pdf"
                    onChange={onFileChange}
                  />

                  {file && (
                    <div className="attached-file">
                      <small>Priloženo: {file.name} ({Math.round(file.size / 1024)} KB)</small>
                    </div>
                  )}

                  <div className="form-actions">
                    <button type="submit" disabled={uploading}>
                      {uploading ? 'Spremanje...' : 'Objavi'}
                    </button>
                    <button type="button" className="close-modal-btn" onClick={() => setShowModal(false)}>Zatvori</button>
                  </div>

                  {message && <p className={styles.message}>{message}</p>}
                </form>

                <button className="close-modal-btn" onClick={() => setShowModal(false)}>Zatvori</button>
              </div>
            </div>
          )}

          <div className={styles.postsList}>
            {posts.length === 0 ? (
              <p className={styles.noPosts}>Još nema objava.</p>
            ) : (
              posts.map((post) => (
                <div key={post.id} className={styles.postItem}>
                  
                  <p>{post.title}</p>
                  <p>{post.post}</p>
                  {post.file && (
                    <p>
                      <a href={post.file} target="_blank" rel="noreferrer">Preuzmi PDF</a>
                    </p>
                  )}
                  <span className="post-date">{post.uploaded_at || post.date}</span>
                </div>
              ))
            )}
          </div>
        </div>
      </main>
    </div>
  );
}