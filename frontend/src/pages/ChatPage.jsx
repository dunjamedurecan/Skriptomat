import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { documentsAPI } from '../api/auth';
import Chat from '../components/Chat';
import styles from '../styles/ChatPage.module.css';
import commonStyles from '../styles/Home.module.css';

export default function ChatPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [document, setDocument] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchDocument = async () => {
      try {
        const data = await documentsAPI.getAll();
        const doc = data.find(d => d.id === parseInt(id));
        if (doc) {
          setDocument(doc);
        } else {
          setError('Dokument nije pronađen');
        }
        setLoading(false);
      } catch (err) {
        console.error('Error fetching document:', err);
        setError('Greška pri učitavanju dokumenta');
        setLoading(false);
      }
    };

    fetchDocument();
  }, [id]);

  if (loading) {
    return (
      <div className={commonStyles.container}>
        <header>
          <h1>Skriptomat</h1>
          <nav className={commonStyles.navbar}>
            <button onClick={logout}>Odjavi se</button>
          </nav>
        </header>
        <div className={styles.loading}>Učitavanje...</div>
      </div>
    );
  }

  if (error || !document) {
    return (
      <div className={commonStyles.container}>
        <header>
          <h1>Skriptomat</h1>
          <nav className={commonStyles.navbar}>
            <button onClick={logout}>Odjavi se</button>
          </nav>
        </header>
        <div className={styles.error}>{error || 'Dokument nije pronađen'}</div>
      </div>
    );
  }

  return (
    <div className={commonStyles.container}>
      <header>
        <h1>Skriptomat</h1>
        <nav className={commonStyles.navbar}>
          <button onClick={() => navigate('/feed')} className={styles.backButton}>
            ← Natrag
          </button>
          <button onClick={logout}>Odjavi se</button>
        </nav>
      </header>

      <main className={styles.chatMain}>
        <div className={styles.chatWrapper}>
          <Chat documentId={document.id} documentTitle={document.title} />
        </div>
      </main>
    </div>
  );
}
