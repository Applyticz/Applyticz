import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const OutlookCallback = () => {
    const navigate = useNavigate();

    useEffect(() => {
        // Capture the authorization code from the URL
        const urlParams = new URLSearchParams(window.location.search);
        // console.log(urlParams);
        const code = urlParams.get("code");
        // console.log(code);

        if (code) {
            // Send the code to the backend to exchange for an access token
            fetch("http://localhost:8000/outlook_api/callback?code=" + code, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
                    "Content-Type": "application/json",
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.access_token) {
                    // Successfully received access token, redirect to the desired page
                    localStorage.setItem("outlook_access_token", data.access_token);
                    navigate("/dashboard"); // Redirect after successful authentication
                } else {
                    console.error("Error fetching access token:", data.error);
                }
            })
            .catch(error => {
                console.error("Error:", error);
            });
        }
    }, [navigate]);

    return (
        <div>
            <h2>Processing Outlook Authentication...</h2>
        </div>
    );
};

export default OutlookCallback;
