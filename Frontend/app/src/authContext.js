import React, { createContext, useState } from "react";

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

  const logoutUser = () => {
    setAuthTokens(null);
    localStorage.removeItem("access_token");
    // console.log("Access token removed.");
  };

  return (
    <AuthContext.Provider value={{ authTokens, loginUser, logoutUser }}>
      {children}
    </AuthContext.Provider>
  );
};
