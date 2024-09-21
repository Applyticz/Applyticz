import React, { createContext, useState } from "react";
import { Navigate } from "react-router-dom";
import axios from "axios"; // Import axios for making HTTP requests

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState(() =>
    localStorage.getItem("access_token"),
  );

  const loginUser = (token) => {
    setAuthTokens(token);
    localStorage.setItem("access_token", token);
    // console.log("Access token set:", token);
  };

  const verifyAuthToken = async () => {
    if (!authTokens) {
      return { status: "no_token" };
    }

    try {
      const response = await axios.post(
        "/verify_token",
        {},
        {
          headers: {
            Authorization: `Bearer ${authTokens}`,
          },
        }
      );
      return response.data;
    } catch (error) {
      console.error("Token verification failed:", error);
      return { status: "invalid" };
    }
  };

  const logoutUser = () => {
    setAuthTokens(null);
    localStorage.removeItem("access_token");
    // console.log("Access token removed.");
  };

  return (
    <AuthContext.Provider value={{ authTokens, loginUser, logoutUser, verifyAuthToken }}>
      {children}
    </AuthContext.Provider>
  );
};
