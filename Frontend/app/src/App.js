import React from "react";
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from "react-router-dom";

import "./App.css";
import Login from "./Pages/Authentication/Login";
import Register from "./Pages/Authentication/Register";
import Dashboard from "./Pages/Dashboard/DashboardPage";
import Applications from "./Pages/MyApplications/ApplicationsPage";
import Resumes from "./Pages/Resumes/ResumesPage";
import Analytics from "./Pages/Analytics/AnalyticsPage";
import Settings from "./Pages/Settings/SettingsPage";
import ProtectedRoutes from "./ProtectedRoutes";
import NavBar from "./Pages/Header/NavBar"; 


/* TODO:
  //Restructure Component Directorys
  //Put signout in Navbar and delete the route, also delete profile
  //Make Applytics not purple anymore

  //Make / and "" redirects go to landing page instead
  //Make Landing Page a little better
  //Delete Unnecessary Routess

  //Coordinate w Alec about authentication for just typing in routes directly

*/

function NotFound() {
  return (
    <div>
      <h2>404 - Page Not Found</h2>
      <p>Oops! The page you are looking for does not exist.</p>
      <Link to="/login">Go back to login</Link>
    </div>
  );
}



// NEED TO ADD AUTHENTICATION TO PROTECTED ROUTES!!!
function ProtectedLayout() {
  return (
    <>
      <NavBar /> {/* NavBar visible across all protected routes */}
      <div className="ProtectedContent">
        <Routes>
          {/* Defined Routes */}
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/applications" element={<Applications />} />
          <Route path="/resumes" element={<Resumes />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/settings" element={<Settings />} />

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
