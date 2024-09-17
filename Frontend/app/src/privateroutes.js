import React, { useContext } from "react";
import { Navigate } from "react-router-dom";
import { AuthContext } from "./authContext";

function PrivateRoute({ element: Component }) {
  const { authTokens } = useContext(AuthContext);

  return authTokens ? <Component /> : <Navigate to="/login" />;
}

export default PrivateRoute;
