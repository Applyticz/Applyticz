import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { AuthContext } from "../../../authContext";

function NavBar() {
  // Call hooks at the top level
  const { logoutUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logoutUser();
    navigate("/login");
  };

  return (
    <nav className="NavBar">
      <ul className="left-nav">
        {/* ... your other navigation links ... */}
        <li>
          <Link to="/">Dashboard</Link>
        </li>
        <li>
          <Link to="/applications">Applications</Link>
        </li>
        <li>
          <Link to="/resumes">Resumes</Link>
        </li>
        <li>
          <Link to="/analytics">Analytics</Link>
        </li>
        <li>
          <Link to="/settings">Settings</Link>
        </li>
      </ul>
      <ul className="right-nav">
        <li>
          <Link to="/profile">Profile</Link>
        </li>
        <li>
          <button className="link-button" onClick={handleLogout}>
            Sign Out
          </button>
        </li>
      </ul>
    </nav>
  );
}

export default NavBar;
