import React,{useState} from "react";
import styles from '../styles/ProfileHover.module.css';
import { Link } from "react-router-dom";

export default function ProfileHover({user}){
    const [showCard,setShowCard]=useState(false);

    const handleMouseEnter=()=>{
        setShowCard(true);
    }

    const handleMouseLeave=()=>{
        setShowCard(false);
    }

    // Handle both string (old format) and object (new format)
    const username = typeof user === 'string' ? user : (user?.username || 'Nepoznato');
    const fullName = typeof user === 'object' && user?.first_name && user?.last_name 
        ? `${user.first_name} ${user.last_name}` 
        : username;

    return(
        <span className={styles.profileContainer}
        onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
            <span className={styles.profileName}>{username}</span>
            {showCard && (
                <div className={styles.profileCard}>
                    <p><strong>{fullName}</strong></p>
                    <p className={styles.usernameText}>@{username}</p>
                    <p className={styles.link}>Pošalji poruku</p>
                    <Link to={`/profile/${username}`} className={styles.link}>Posjeti profil</Link>
                </div>
            )}
        </span>
    )
}