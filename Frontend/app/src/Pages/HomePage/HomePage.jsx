import React, { useContext, useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { AuthContext } from "../../authContext";

function Header() {
  return (
    <header className="Header">
      <h2>Applytics</h2>
    </header>
  );
}

function NavBar() {
  return (
    <nav className="NavBar">
      <ul className="left-nav">
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
          <Link to="/sign-out">Sign Out</Link>
        </li>
      </ul>
    </nav>
  );
}

function HomePage() {
  const { authTokens } = useContext(AuthContext);
  const [userData, setUserData] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");

  const getUserData = async () => {
    if (!authTokens) {
      setErrorMessage("Access token not found.");
      return;
    }
    try {
      const response = await fetch("http://localhost:8000", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${authTokens}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        console.log("User data:", data);
        setUserData(data);
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.detail || "Failed to fetch user data.");
      }
    } catch (error) {
      console.error("Error:", error);
      setErrorMessage("An error occurred. Please try again.");
    }
  };

  useEffect(() => {
    getUserData();
  }, []); // Fetch user data on component mount

  return (
    <div className="App">
      <Header />
      <NavBar />
      <div className="Content">
        <button onClick={getUserData}>Get User Data</button>
        {userData && (
          <div>
            <h2>User Data</h2>
            <p>Username: {userData.User.id}</p>
            <p>Email: {userData.User.username}</p>
          </div>
        )}
        {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
      </div>
    </div>
  );
}

export default HomePage;
