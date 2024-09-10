import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';

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

function Dashboard() {
  return <h1>Dashboard</h1>;
}

function Applications() {
  return <h1>Applications</h1>;
}

function Resumes() {
  return <h1>Resumes</h1>;
}

function Analytics() {
  return <h1>Analytics</h1>;
}

function Settings() {
  return <h1>Settings</h1>;
}

function Profile() {
  return <h1>Profile</h1>;
}

function SignOut() {
  return <h1>Sign Out</h1>;
}

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <NavBar />
        <div className="Content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/applications" element={<Applications />} />
            <Route path="/resumes" element={<Resumes />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/sign-out" element={<SignOut />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
