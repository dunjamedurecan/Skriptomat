import {Link} from "react-router-dom";

export default function Feed(){
    return(
    <div className="container">
        <header>
            <h1><Link to="/">Skriptomat</Link></h1>
            <nav className="navbar">
                <Link to="/">Profil</Link>
                <Link to="/">Odjava</Link>
            </nav>
        </header>

    </div>);
}