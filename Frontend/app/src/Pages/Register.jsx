// src/Pages/Login.jsx
import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../authContext";

const Register = () => {
  const navigate = useNavigate();
  const { registerUser } = useContext(AuthContext);
  const [errorMessage, setErrorMessage] = useState("");

  // Inside your Register component
  const submitRegister = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(
        "http://localhost:8000/auth/register_account",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: e.target.username.value,
            email: e.target.email.value,
            password: e.target.password.value,
          }),
        }
      );

      if (response.ok) {
        const data = await response.json();
        console.log("Success:", data);
        // Handle successful registration
      } else {
        const errorData = await response.json();
        console.error("Error:", errorData.detail);
        // Display error message to the user
      }
    } catch (error) {
      console.error("Error:", error);
      // Handle network errors
    }
  };

  return (
    <div>
      <h2>Register</h2>
      {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
      <form onSubmit={submitRegister}>
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
            Email:
            <input type="text" name="email" required autoComplete="email" />
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
        <button type="submit">Register</button>
      </form>
    </div>
  );
};

export default Register;
