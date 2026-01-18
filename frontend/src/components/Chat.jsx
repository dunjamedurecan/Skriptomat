import React, { useState, useEffect, useRef } from 'react';
import { db } from '../firebase';
import { collection, addDoc, query, orderBy, onSnapshot, serverTimestamp } from 'firebase/firestore';
import { useAuth } from '../context/AuthContext';
import styles from '../styles/Chat.module.css';

const DocumentChat = ({ documentId, documentTitle }) => {
  const { user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const messagesEndRef = useRef(null);

  // Scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Listen to messages in real-time
  useEffect(() => {
    if (!documentId) return;

    const messagesRef = collection(db, 'documents', String(documentId), 'messages');
    const q = query(messagesRef, orderBy('timestamp', 'asc'));

    const unsubscribe = onSnapshot(q, (snapshot) => {
      const msgs = snapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
      setMessages(msgs);
      setLoading(false);
    });

    return () => unsubscribe();
  }, [documentId]);

  // Send a new message
  const handleSendMessage = async (e) => {
    e.preventDefault();
    
    if (!newMessage.trim()) return;

    try {
      const messagesRef = collection(db, 'documents', String(documentId), 'messages');
      await addDoc(messagesRef, {
        text: newMessage,
        userId: user?.id || user?.username,
        username: user?.username || 'Anonymous',
        timestamp: serverTimestamp()
      });

      setNewMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
      alert('Greška pri slanju poruke');
    }
  };

  if (loading) {
    return <div className={styles.loading}>Učitavanje diskusije...</div>;
  }

  return (
    <div className={styles.chatContainer}>
      <div className={styles.chatHeader}>
        <h3>💬 Diskusija: {documentTitle}</h3>
      </div>

      <div className={styles.messagesContainer}>
        {messages.length === 0 ? (
          <p className={styles.noMessages}>Još nema poruka. Budi prvi!</p>
        ) : (
          messages.map((msg) => (
            <div 
              key={msg.id} 
              className={`${styles.message} ${msg.userId === (user?.id || user?.username) ? styles.myMessage : styles.otherMessage}`}
            >
              <div className={styles.messageHeader}>
                <span className={styles.username}>{msg.username}</span>
                <span className={styles.timestamp}>
                  {msg.timestamp?.toDate().toLocaleTimeString('hr-HR', { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
              <div className={styles.messageText}>{msg.text}</div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSendMessage} className={styles.inputContainer}>
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Napiši poruku..."
          className={styles.input}
        />
        <button type="submit" className={styles.sendButton}>
          Pošalji
        </button>
      </form>
    </div>
  );
};

export default DocumentChat;
