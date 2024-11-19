import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";

const GmailCallback = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Capture the authorization code from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get("code");

    if (code) {
      // Send the code to the backend to exchange for an access token
      fetch(`http://localhost:8000/gmail_api/callback?code=${code}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
        },
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Backend response:", data); // Log the entire response

          if (data.access_token) {
            // Store the Gmail access token in localStorage
            localStorage.setItem("gmail_access_token", data.access_token);
            navigate("/dashboard"); // Redirect after successful authentication
          } else {
            console.error(
              "Error fetching access token:",
              data.error || "Access token not present"
            );
          }
        })
        .catch((error) => {
          console.error("Error during token exchange:", error);
        });
    } else {
      console.error("Authorization code not found in URL");
    }
  }, [navigate]);

  return (
    <div>
      <h2>Processing Gmail Authentication...</h2>
    </div>
  );
};

export default GmailCallback;
