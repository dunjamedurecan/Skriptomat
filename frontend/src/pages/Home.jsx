import { Link } from "react-router-dom";
import styles from '../styles/Home.module.css'

export default function Home() {
  return (
    <div className={styles.container}>
        <header>
            <h1>Skriptomat</h1>
            <nav className={styles.navbar}>
                <Link to="/login">Prijava</Link>
                <Link to="/registration">Registracija</Link>
                <Link to="/about">O nama</Link>
            </nav>
        </header>
        <main>
            <section className={styles.banner}>
                <div className={styles.content}>
                     <h1>Dobrodošli u Skriptomat</h1>
                <p>Dijeli svoje skripte. Inspiriraj druge. Brzo i jednostavno.</p>
                </div>
            </section>
        </main>
    </div>
  );
}
