import { Link } from "react-router-dom";

function PublicHeader() {
    return (
        <header className="Header">
        <h2>
            <Link to="/landing" className="Header">Applyticz</Link>  
        </h2>
        </header>
    );
}

export default PublicHeader;