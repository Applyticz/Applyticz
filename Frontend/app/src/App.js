import React, { useContext, useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import "./App.css";
import Login from "./Pages/Login";
import Register from "./Pages/Register";
import Dashboard from "./Pages/HomePage/HomePageComponents/Dashboard";
import Applications from "./Pages/HomePage/HomePageComponents/Applications";
import Resumes from "./Pages/HomePage/HomePageComponents/Resumes";
import Analytics from "./Pages/HomePage/HomePageComponents/Analytics";
import Settings from "./Pages/HomePage/HomePageComponents/Settings";
import Profile from "./Pages/HomePage/HomePageComponents/Profile";
import SignOut from "./Pages/HomePage/HomePageComponents/SignOut";
import HomePage from "./Pages/HomePage/HomePage";


function App() {
  return (
    <Router>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/home" element={<HomePage />} />
            <Route path="/" element={<Dashboard />} />
            <Route path="/applications" element={<Applications />} />
            <Route path="/resumes" element={<Resumes />} />
            <Route path="/analytics" element={<Analytics />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/sign-out" element={<SignOut />} />
          </Routes>
    </Router>
  );
}

export default App;
