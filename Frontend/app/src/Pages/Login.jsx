// src/Pages/Login.jsx
import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../authContext";

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
        navigate("/"); // Redirect to the home page or dashboard
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
    <div>
      <h2>Login</h2>
      {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
      <form onSubmit={submitLogin}>
        <div>
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
        <div>
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
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
