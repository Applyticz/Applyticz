import React, { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { AuthContext } from "../../authContext";
import "./Auth.css"; // Import the CSS file for styling
import PublicHeader from '../Landing/PublicHeader';

const Login = () => {
  const navigate = useNavigate();
  const { loginUser } = useContext(AuthContext);
  const [errorMessage, setErrorMessage] = useState("");

  const submitLogin = async (e) => {
    e.preventDefault();
    try {
      // Handle app login first
      const response = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: e.target.username.value,
          password: e.target.password.value,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        loginUser(data.access_token); // Save the app access token in the Auth context

        // Redirect to the Outlook OAuth2 login endpoint
          window.location.href = `http://localhost:8000/outlook_api/login?state=${data.access_token}`;
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.detail || "Failed to login.");
      }
    } catch (error) {
      console.error("Error:", error);
      setErrorMessage("An error occurred. Please try again.");
    }
  };

  return (
    <>
      <PublicHeader />
      <div className="auth-container">
        <h2>Login</h2>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
        <form onSubmit={submitLogin} className="auth-form">
          <div className="form-group">
            <label>
              Username:
              <input
                type="text"
                name="username"
                required
                autoComplete="username"
              />
            </label>
          </div>
          <div className="form-group">
            <label>
              Password:
              <input
                type="password"
                name="password"
                required
                autoComplete="current-password"
              />
            </label>
          </div>
          <button type="submit" className="auth-button">Login</button>
        </form>
        <p className="switch-auth">
          Don't have an account? <Link to="/register">Register here</Link>
        </p>
      </div>
    </>
  );
};

export default Login;
