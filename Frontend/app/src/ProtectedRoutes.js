// ProtectedRoutes.js
import React, { useContext } from "react";
import { Navigate, Outlet } from "react-router-dom";
import { AuthContext } from "./authContext";

const ProtectedRoute = () => {
  const { authTokens } = useContext(AuthContext);

  return authTokens ? <Outlet /> : <Navigate to="/login" />;
};

export default ProtectedRoute;
