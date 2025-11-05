import { Link } from "react-router-dom";
import styles from '../styles/Home.module.css';

export default function About() {
  return (
    <div className={styles.container}>
        <header>
            <h1>O nama</h1>
            <nav className={styles.navbar}>
                <Link to="/">Početna</Link>
                <Link to="/login">Prijava</Link>
                <Link to="/registration">Registracija</Link>
            </nav>
        </header>
    </div>
  );
}