import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import '../styles/feed.css'

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
    <div className="container">
      <header>
        <h1>Skriptomat</h1>
        <nav className="navbar">
          <Link to="/">Profil</Link>
          <Link to="/">Odjava</Link>
        </nav>
      </header>

      <main className="feed-main">
        <div className="feed-card">
          <button className="open-modal-btn" onClick={() => setShowModal(true)}>Nova objava</button>

          {showModal && (
            <div className="modal-overlay" onClick={() => setShowModal(false)}>
              <div className="modal" onClick={(e) => e.stopPropagation()}>
                <h3>Napiši novu objavu</h3>
                <form className="new-post-form" onSubmit={handleAddPost}>
                  <textarea
                    value={newPost}
                    onChange={(e) => setNewPost(e.target.value)}
                    placeholder="Unesi sadržaj objave..."
                  ></textarea>
                  <button type="submit">Objavi</button>
                </form>
                <button className="close-modal-btn" onClick={() => setShowModal(false)}>Zatvori</button>
              </div>
            </div>
          )}

          <div className="posts-list">
            {posts.length === 0 ? (
              <p className="no-posts">Još nema objava.</p>
            ) : (
              posts.map((post) => (
                <div key={post.id} className="post-item">
                  <p>{post.content}</p>
                  <span className="post-date">{post.date}</span>
                </div>
              ))
            )}
          </div>
        </div>
      </main>
    </div>
  )
}