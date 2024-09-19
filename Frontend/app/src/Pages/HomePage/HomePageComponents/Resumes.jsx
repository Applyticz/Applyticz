import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom"; // Correctly import useNavigate
import { AuthContext } from "../../../authContext";
import NavBar from "./NavBar";


function Resumes() {
  const { authTokens } = useContext(AuthContext);
  const [resumeData, setResumeData] = useState(null);
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate(); // Correctly use navigate here

  const getValidToken = async () => {
    if (!authTokens) {
      navigate("/login");
      console.log("Access token not found.");
    } else {
      console.log("Access token found:", authTokens);
    }
  };

  const getResumeData = async () => {
    if (!authTokens) {
      setErrorMessage("Access token not found.");
      return;
    }
    try {
      const response = await fetch("http://localhost:8000/resume/get_resumes", {
        // Correct API endpoint
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${authTokens}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        console.log("Resume data:", data);
        setResumeData(data);
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
  }, []); // Only run the effect once when the component mounts

  return (
    <div className="App">
      <div className="Content">
        <button onClick={getResumeData}>Get Resume Data</button>
        {resumeData && (
          <div>
            <h2>Resume Data</h2>
            <ul>
              {resumeData.map((resume) => (
                <li key={resume.id}>
                  <p>Resume Title: {resume.title}</p>
                  <p>Resume Description: {resume.description}</p>
                  <p>Resume Date: {resume.date}</p>
                  <p>Resume URL: {resume.pdf_url}</p>
                </li>
              ))}
            </ul>
          </div>
        )}
        {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
      </div>
    </div>
  );
}

export default Resumes;
