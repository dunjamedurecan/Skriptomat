import { Link } from "react-router-dom";

export default function About() {
  return (
    <div className="container">
        <header>
            <h1>O nama</h1>
            <nav className="navbar">
                <Link to="/">Početna</Link>
            </nav>
        </header>
    </div>
  );
}