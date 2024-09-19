import React, { useContext } from "react";
import { Navigate, Outlet } from "react-router-dom";
import { AuthContext } from "./authContext";

const ProtectedRoutes = () => {
  // Use the useContext hook to access the AuthContext
  const { authTokens } = useContext(AuthContext);

  if (!authTokens) {
    // If not authenticated, redirect to login
    //console.log("Access token not found.");
    return <Navigate to="/login" />;
  }

  // If authenticated, render child routes
  //console.log("Access token found:", authTokens);
  return <Outlet />;
};

export default ProtectedRoutes;
