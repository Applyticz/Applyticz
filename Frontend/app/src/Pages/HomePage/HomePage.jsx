import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom"; // Correctly import useNavigate
import { AuthContext } from "../../authContext";



function HomePage() {
  const { authTokens } = useContext(AuthContext);
  const [userData, setUserData] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate();

  const getValidToken = async () => {
    if (!authTokens) {
      navigate("/login");
      console.log("Access token not found.");
    } else {
      console.log("Access token found:", authTokens);
    }
  };

  const getUserData = async () => {
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
        console.log("User data:", data);
        setUserData(data);
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.detail || "Failed to fetch user data.");
      }
    } catch (error) {
      console.error("Error:", error);
      setErrorMessage("An error occurred. Please try again.");
    }
  };

  useEffect(() => {
    getValidToken();
  }); // Fetch use

  return (
    <div className="App">
      <div className="Content">
        <button onClick={getUserData}>Get User Data</button>
        {userData && (
          <div>
            <h2>User Data</h2>
            <p>Email: {userData.email}</p>
            <p>Username: {userData.username}</p>
          </div>
        )}
        {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
      </div>
    </div>
  );
}

export default HomePage;
