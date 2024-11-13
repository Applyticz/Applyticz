import { useContext } from "react";
import { useNavigate } from "react-router-dom";

// Custom hook to access auth tokens and validate them
function useAuth() {
  const authTokens = localStorage.getItem('access_token');
  const navigate = useNavigate(); // Hook to navigate if token is invalid

  const getValidToken = async () => {
    try {
      const response = await fetch(`http://localhost:8000/auth/verify-token/${authTokens}`);
      if (!response.ok) {
        throw new Error('Token verification failed');
      }
      if (!authTokens) {
        console.log("Access token not found.");
        navigate("/login"); // Redirect to login if no token is found
      } else {
        // console.log("Access token found:", authTokens);
        return authTokens; // Return the valid auth token
      }
    } catch (error) {
      localStorage.removeItem('access_token');
      navigate('/login');
    }
  };

  return { authTokens, getValidToken }; // Return both authTokens and getValidToken
}

export default useAuth;
