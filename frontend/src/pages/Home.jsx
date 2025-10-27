import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div className="container">
        <header>
            <h1>Skriptomat</h1>
            <nav className="navbar">
                <Link to="/login">Prijava</Link>
                <Link to="/registration">Registracija</Link>
                <Link to="/about">O nama</Link>
            </nav>
        </header>
        <main>
            <section className="banner">
                <div className="content">
                     <h1>Dobrodošli u Skriptomat</h1>
                <p>Dijeli svoje skripte. Inspiriraj druge. Brzo i jednostavno.</p>
                </div>
            </section>
        </main>
    </div>
  );
}
