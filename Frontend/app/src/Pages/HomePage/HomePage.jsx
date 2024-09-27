import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom"; // Correctly import useNavigate
import { AuthContext } from "../../authContext";
import useAuth from "../../utils";

function HomePage() {
  const { authTokens, getValidToken } = useAuth(); // Use the custom hook to access auth tokens
  const [userData, setUserData] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  const getUserData = async () => {
    //console.log(authTokens);
    if (!authTokens) {
      setErrorMessage("Access token not found.");
      return;
    }
    try {
      const response = await fetch("http://localhost:8000/auth/get_account", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${authTokens}`,
        },
      });

      if (response.ok) {
        const data = await response.json();

        // Validate the response data against the expected model structure
        if (
          data &&
          typeof data.username === "string" &&
          typeof data.email === "string"
        ) {
          //console.log("User data:", data);
          setUserData(data);
        } else {
          setErrorMessage("Invalid data format received.");
        }
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.detail || "Failed to fetch user data.");
      }
    } catch (error) {
      //console.error("Error:", error);
      setErrorMessage("An error occurred. Please try again.");
    }
  };

  useEffect(() => {
    getValidToken(); // Call getValidToken to check if the token is valid
  });

  return (
    <div className="App">
      <div className="Content">
        <button onClick={getUserData}>Get User Data</button>
        {userData && (
          <div>
            <h2>User Information</h2>
            <p>Username: {userData.username}</p>
            <p>Email: {userData.email}</p>
          </div>
        )}
        {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
      </div>
    </div>
  );
}

export default HomePage;
