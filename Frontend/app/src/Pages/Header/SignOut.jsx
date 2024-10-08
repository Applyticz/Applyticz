// src/Pages/SignOut.jsx
import React, { useEffect, useContext } from "react";
import { AuthContext } from "../../authContext";
import { useNavigate } from "react-router-dom";

function SignOut() {
  const { logoutUser } = useContext(AuthContext);
  const navigate = useNavigate();

  useEffect(() => {
    logoutUser();
    navigate("/login");
  }, [logoutUser, navigate]);

  return null; // Or display a message if desired
}

export default SignOut;
