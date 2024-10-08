import React from "react";
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from "react-router-dom";

import "./App.css";

import Login from "./Pages/Authentication/Login";
import Register from "./Pages/Authentication/Register";
import Dashboard from "./Pages/HomePage/HomePageComponents/Dashboard";
import Applications from "./Pages/MyApplications/ApplicationsPage";
import Resumes from "./Pages/HomePage/HomePageComponents/Resumes";
import Analytics from "./Pages/HomePage/HomePageComponents/Analytics";
import Settings from "./Pages/HomePage/HomePageComponents/Settings";
import Profile from "./Pages/HomePage/HomePageComponents/Profile";
import SignOut from "./Pages/HomePage/HomePageComponents/SignOut";
import ProtectedRoutes from "./ProtectedRoutes";
import NavBar from "./Pages/HomePage/HomePageComponents/NavBar"; // NavBar imported here


function NotFound() {
  return (
    <div>
      <h2>404 - Page Not Found</h2>
      <p>Oops! The page you are looking for does not exist.</p>
      <Link to="/">Go back to the homepage</Link>
    </div>
  );
}

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
          {/* Defined Routes */}
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/applications" element={<Applications />} />
          <Route path="/resumes" element={<Resumes />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/sign-out" element={<SignOut />} />

          {/* All Other Routes - 404 Error */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        {/* UnAuthenticated Routes */}
        <Route path="/" element={<Navigate to ="/login" />} />
        <Route path="" element={<Navigate to ="/login" />} />

        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />


        {/* All Other Routes */}
        <Route element={<ProtectedRoutes />}>
          <Route path="/*" element={<ProtectedLayout />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
