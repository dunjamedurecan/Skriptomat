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

    return(
        <div className={styles.profileContainer}
        onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
            <span className={styles.profileName}>{user}</span>
            {showCard && (
                <div className={styles.profileCard}>
                    <p><strong>{user}</strong></p>
                    <p className={styles.link}>Pošalji poruku</p>
                    <Link to={`/profile/${user}`} className={styles.link}>Posjeti profil</Link>
                </div>
            )}
        </div>
    )
}