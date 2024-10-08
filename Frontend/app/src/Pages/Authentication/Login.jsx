// src/Pages/Login.jsx
import React, { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { AuthContext } from "../../authContext";
import "./Auth.css"; // Import the CSS file for styling

const Login = () => {
  const navigate = useNavigate();
  const { loginUser } = useContext(AuthContext);
  const [errorMessage, setErrorMessage] = useState("");

  const submitLogin = async (e) => {
    e.preventDefault();
    try {
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
        loginUser(data.access_token); // Update authentication context
        navigate("/dashboard"); // Redirect to the home page or dashboard
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
  );
};

export default Login;
