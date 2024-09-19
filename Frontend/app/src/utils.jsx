import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "./authContext";

// Custom hook to access auth tokens and validate them
function useAuth() {
  const { authTokens } = useContext(AuthContext); // Access tokens from AuthContext
  const navigate = useNavigate(); // Hook to navigate if token is invalid

  const getValidToken = async () => {
    if (!authTokens) {
      console.log("Access token not found.");
      navigate("/login"); // Redirect to login if no token is found
    } else {
      console.log("Access token found:", authTokens);
      return authTokens; // Return the valid auth token
    }
  };

  return { authTokens, getValidToken }; // Return both authTokens and getValidToken
}

export default useAuth;
