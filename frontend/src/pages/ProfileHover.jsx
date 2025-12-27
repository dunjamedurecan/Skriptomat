import React,{useState} from "react";
import styles from '../styles/ProfileHover.module.css';

export default function ProfileHover({user}){
    const [showCard,setShowCard]=useState(false);

    const handleMouseEnter=()=>{
        setShowCard(true);
    }

    const handleMouseLeave=()=>{
        setShowCard(false);
    }

    return(
        <div className={styles.profileContainer}
        onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
            <span className={styles.profileName}>{user}</span>
            {showCard && (
                <div className={styles.profileCard}>
                    <p><strong>{user}</strong></p>
                    <button className={styles.messageBtn}>Pošalji poruku</button>
                    <button className={styles.visitBtn}>Posjeti profil</button>
                </div>
            )}
        </div>
    )
}