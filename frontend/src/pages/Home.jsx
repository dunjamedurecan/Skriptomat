import {Link} from "react-router-dom";
export default function Home(){
    return (
    <body>
        <h1>Skriptomat</h1>
        <nav className="navbar">
            <Link to="about">O nama</Link>
        </nav>
    </body>
    );
}