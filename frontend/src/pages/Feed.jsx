import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import '../styles/feed.css'

export default function Feed() {
  const [posts, setPosts] = useState([])
  const [newPost, setNewPost] = useState('')
  const [showModal, setShowModal] = useState(false)

  //PDF-upload
  const[file,setFile]=useState(null)
  const [uploading,setUploading]=useState(false)
  const fileInputRef=useRef(null)

  const API_BASE='http://localhost:8000/api'

  useEffect(()=>{
    fetchPosts()
  },[])
  const fetchPosts=async()=>{
    try{
      const res=await fetch(`${API_BASE}/posts/`)
      if(!res.ok)throw new Error('Ne mogu dohvatiti objave')
      const data=await res.json()
      setPosts(data)
    }catch(err){
      console.error('fetchPosts error',err)
    }
  }
  const handleFileChange=(e)=>{
    const f=e.target.files[0]
    setFile(f||null)
  }
  const handleAddPost = async(e) => {
    e.preventDefault()
    if (newPost.trim() === ''&&!file){
      return alert('Unesi sadržaj objave ili priloži PDF.')
    }

    const formData=new FormData()
    formData.append('content',newPost)
    if(file){
      formData.append('file',file)
    }else{
      return alert('Priloži pdf datoteku')
    }
    try{
      setUploading(true)
      const res=await fetch(`${API_BASE}/posts/`,{
        method:'POST',
        body:formData
      })
      if(!res.ok){
        const err=await res.json().catch(()=>null)
        console.error('Upload/Save post error',err)
        return
      }
      const savedPost=await res.json()
      setPosts(prev=>[savedPost,...prev])
      setNewPost('')
      setFile(null)
      if(fileInputRef.current)fileInputRef.current.value=''
      setShowModal(false)
    }catch(err){
      console.error('handlaAddPost error',err)
    }finally{
      setUploading(false)
    }
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
                  <hr/>
                  <h4>Priloži PDF</h4>
                  <input ref={fileInputRef} type="file" accept="application/pdf" onChange={handleFileChange}/>
                  {file && (
                    <div className="attached-file">
                      <small>Priloženo: {file.name} ({Math.round(file.size/1024)}KB)</small>
                    </div>
                  )}
                  <div className='form-actions'>
                    <button type="submit" disabled={uploading}>
                      {uploading ? 'Spremanje...':'Objavi'}
                    </button>
                    <button type="button" className='close-modal-btn' onClick={()=>setShowModal(false)}>Zatvori</button>
                  </div>
                </form>
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

                  {post.file &&(
                    <div className='post-file'>
                      <span>{post.file.filename}({Math.round((post.file.size||0)/1024)}KB</span>
                      {post.file.download_url ? (
                        <button onClick={()=>handleDownload(post.file.download_url,post.file.filename)}>Preuzmi</button>

                      ):(
                        <button onClick={()=>handleDownload(`${API_BASE}/posts/${post.id}/download/`,post.file.filename)}>Preuzmi</button>
                      )}
                      </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      </main>
    </div>
  )
}