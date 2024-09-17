// ProtectedRoutes.js
import React, { useContext } from "react";
import { Navigate, Outlet } from "react-router-dom";
import { AuthContext } from "./authContext";


const ProtectedRoutes = () => {
  const { authTokens } = AuthContext;

  if (!authTokens) {
    // If not authenticated, redirect to login
    return <Navigate to="/login" />;
  }

  // If authenticated, render child routes
  return <Outlet />;
};

export default ProtectedRoutes;
