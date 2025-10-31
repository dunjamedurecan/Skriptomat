import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import styles from '../styles/Feed.module.css'
import commonStyles from '../styles/Home.module.css'

export default function Feed() {
  const [posts, setPosts] = useState([])
  const [newPost, setNewPost] = useState('')
  const [showModal, setShowModal] = useState(false)

  const handleAddPost = (e) => {
    e.preventDefault()
    if (newPost.trim() === '') return
    const post = {
      id: Date.now(),
      content: newPost.trim(),
      date: new Date().toLocaleString()
    }
    setPosts([post, ...posts])
    setNewPost('')
    setShowModal(false)
  }

  return (
    <div className={commonStyles.container}>
      <header>
        <h1>Skriptomat</h1>
        <nav className={commonStyles.navbar}>
          <Link to="/">Profil</Link>
          <Link to="/">Odjava</Link>
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
                  <button type="submit">Objavi</button>
                </form>
                <button className={styles.closeModalBtn} onClick={() => setShowModal(false)}>Zatvori</button>
              </div>
            </div>
          )}

          <div className={styles.postsList}>
            {posts.length === 0 ? (
              <p className={styles.noPosts}>Još nema objava.</p>
            ) : (
              posts.map((post) => (
                <div key={post.id} className={styles.postItem}>
                  <p>{post.content}</p>
                  <span className={styles.postDate}>{post.date}</span>
                </div>
              ))
            )}
          </div>
        </div>
      </main>
    </div>
  )
}