import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import "./App.css";
import Login from "./Pages/Authentication/Login";
import Register from "./Pages/Authentication/Register";
import Dashboard from "./Pages/HomePage/HomePageComponents/Dashboard";
import Applications from "./Pages/MyApplications/Applications";
import Resumes from "./Pages/HomePage/HomePageComponents/Resumes";
import Analytics from "./Pages/HomePage/HomePageComponents/Analytics";
import Settings from "./Pages/HomePage/HomePageComponents/Settings";
import Profile from "./Pages/HomePage/HomePageComponents/Profile";
import SignOut from "./Pages/HomePage/HomePageComponents/SignOut";
import ProtectedRoutes from "./ProtectedRoutes";
import NavBar from "./Pages/HomePage/HomePageComponents/NavBar"; // NavBar imported here
import HomePage from "./Pages/HomePage/HomePage";

// Create a wrapper component for Protected Routes
function ProtectedLayout() {
  function Header() {
    return (
      <header className="Header">
        <h2>
          <Link to="/">Applyticz</Link>
        </h2>
      </header>
    );
  }

  return (
    <>
      <Header />
      <NavBar /> {/* NavBar visible across all protected routes */}
      <div className="ProtectedContent">
        <Routes>
          {/* Protected routes go here */}
          <Route path="/" element={<HomePage />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/applications" element={<Applications />} />
          <Route path="/resumes" element={<Resumes />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/sign-out" element={<SignOut />} />
        </Routes>
      </div>
    </>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        {/* Wrap Protected Routes with ProtectedLayout */}
        <Route element={<ProtectedRoutes />}>
          <Route path="/*" element={<ProtectedLayout />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
