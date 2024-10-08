import React, { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { AuthContext } from "../../authContext";
import "./Auth.css"; // Import the CSS file for styling
import AuthHeader from './AuthHeader';

const Register = () => {
  const navigate = useNavigate();
  const { registerUser } = useContext(AuthContext);
  const [errorMessage, setErrorMessage] = useState("");

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
        //console.log("Success:", data);
        navigate("/login");
        // Handle successful registration
      } else {
        const errorData = await response.json();
        console.error("Error:", errorData.detail);
        setErrorMessage(errorData.detail || "Failed to register.");
      }
    } catch (error) {
      console.error("Error:", error);
      setErrorMessage("An error occurred. Please try again.");
    }
  };

  return (
    <>
      <AuthHeader />
      <div className="auth-container">
        <h2>Register</h2>
        {errorMessage && <p className="error-message">{errorMessage}</p>}
        <form onSubmit={submitRegister} className="auth-form">
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
              Email:
              <input type="text" name="email" required autoComplete="email" />
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
          <button type="submit" className="auth-button">Register</button>
        </form>
        <p className="switch-auth">
          Already have an account? <Link to="/login">Login here</Link>
        </p>
      </div>
    </>
  );
};

export default Register;
