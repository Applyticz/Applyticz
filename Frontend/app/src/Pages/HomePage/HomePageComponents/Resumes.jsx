import React, { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom"; // Correctly import useNavigate
import useAuth from "../../../utils";
import "./Resume.css";

function Resumes() {
  const { authTokens, getValidToken } = useAuth(); // Use the custom hook to access auth tokens
  const [resumeData, setResumeData] = useState([]); // Initialize as an empty array
  const [errorMessage, setErrorMessage] = useState("");
  const navigate = useNavigate(); // Correctly use navigate here

  const [creatingResume, setCreatingResume] = useState(false); // Track if a new resume is being created
  const [editingResume, setEditingResume] = useState(null); // Track the resume being edited
  const [newTitle, setNewTitle] = useState("");
  const [newDescription, setNewDescription] = useState("");
  const [newDate, setNewDate] = useState("");
  const [newPdfUrl, setNewPdfUrl] = useState("");

  const handleCreateClick = () => {
    setCreatingResume(true);
    setEditingResume(null); // Reset any editing state
    setNewTitle("");
    setNewDescription("");
    setNewDate("");
    setNewPdfUrl("");
  };

  const handleEditClick = (resume) => {
    setEditingResume(resume);
    setCreatingResume(false); // Ensure we hide the create form
    setNewTitle(resume.title);
    setNewDescription(resume.description);
    setNewDate(resume.date);
    setNewPdfUrl(resume.pdf_url);
  };

  const createResume = async () => {
    if (!authTokens) {
      setErrorMessage("Access token not found.");
      return;
    }
    try {
      const response = await fetch(
        "http://localhost:8000/resume/upload_resume",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authTokens}`,
          },
          body: JSON.stringify({
            title: newTitle,
            description: newDescription,
            date: newDate,
            pdf_url: newPdfUrl,
          }),
        }
      );
      if (response.ok) {
        const data = await response.json();
        console.log("Resume created:", data);
        setResumeData((prevResumes) => [...prevResumes, data]);
        setCreatingResume(false); // Hide the form after success
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.detail || "Failed to create resume.");
      }
    } catch (error) {
      console.error("Error:", error);
      setErrorMessage("An error occurred. Please try again.");
    }
  };

  const updateResume = async () => {
    if (!authTokens) {
      setErrorMessage("Access token not found.");
      return;
    }
    try {
      const response = await fetch(
        `http://localhost:8000/resume/update_resume?title=${editingResume.title}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authTokens}`,
          },
          body: JSON.stringify({
            title: newTitle,
            description: newDescription,
            date: newDate,
            pdf_url: newPdfUrl,
          }),
        }
      );
      if (response.ok) {
        const updatedResume = {
          ...editingResume,
          title: newTitle,
          description: newDescription,
          date: newDate,
          pdf_url: newPdfUrl,
        };

        console.log("Updated Resume:", updatedResume);

        // Update the resume data in the state
        setResumeData((prevResumes) =>
          prevResumes.map((resume) =>
            resume.id === editingResume.id ? updatedResume : resume
          )
        );

        setEditingResume(null); // Reset the editing state after success
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.detail || "Failed to update resume.");
      }
    } catch (error) {
      console.error("Error:", error);
      setErrorMessage("An error occurred. Please try again.");
    }
  };

  const getResumeData = async () => {
    if (!authTokens) {
      setErrorMessage("Access token not found.");
      return;
    }
    try {
      const response = await fetch("http://localhost:8000/resume/get_resumes", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${authTokens}`,
        },
      });
      if (response.ok) {
        const data = await response.json();

        // Log the resume data to ensure it's unique
        console.log("Fetched Resume Data:", data);

        // Set the data only once, ensuring no duplication
        setResumeData(data); // Directly set the fetched data
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.detail || "Failed to fetch resume data.");
      }
    } catch (error) {
      console.error("Error:", error);
      setErrorMessage("An error occurred. Please try again.");
    }
  };

  const deleteResume = async (resumeTitle) => {
    if (!authTokens) {
      setErrorMessage("Access token not found.");
      return;
    }
    try {
      const response = await fetch(
        `http://localhost:8000/resume/delete_resume?title=${resumeTitle}`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authTokens}`,
          },
        }
      );
      if (response.ok) {
        setResumeData((prevResumes) =>
          prevResumes.filter((resume) => resume.title !== resumeTitle)
        );
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.detail || "Failed to delete resume.");
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
        <button onClick={handleCreateClick}>Create New Resume</button>
        {resumeData && (
          <div>
            <h2>Resume Data</h2>
            <div>
              {resumeData.map((resume) => (
                <div key={resume.id} className="resume-item">
                  {/* Ensure resume.id is unique */}
                  <p>Resume Title: {resume.title}</p>
                  <p>Resume Description: {resume.description}</p>
                  <p>Resume Date: {resume.date}</p>
                  <p>Resume URL: {resume.pdf_url}</p>
                  <button onClick={() => deleteResume(resume.title)}>
                    Delete
                  </button>
                  <button onClick={() => handleEditClick(resume)}>Edit</button>
                </div>
              ))}
            </div>
          </div>
        )}
        {creatingResume && (
          <div>
            <h2>Create Resume</h2>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                createResume();
              }}
            >
              <div>
                <label>
                  Title:
                  <input
                    type="text"
                    value={newTitle}
                    onChange={(e) => setNewTitle(e.target.value)}
                  />
                </label>
              </div>
              <div>
                <label>
                  Description:
                  <input
                    type="text"
                    value={newDescription}
                    onChange={(e) => setNewDescription(e.target.value)}
                  />
                </label>
              </div>
              <div>
                <label>
                  Date:
                  <input
                    type="date"
                    value={newDate}
                    onChange={(e) => setNewDate(e.target.value)}
                  />
                </label>
              </div>
              <div>
                <label>
                  PDF URL:
                  <input
                    type="text"
                    value={newPdfUrl}
                    onChange={(e) => setNewPdfUrl(e.target.value)}
                  />
                </label>
              </div>
              <button type="submit">Create Resume</button>
            </form>
          </div>
        )}
        {editingResume && (
          <div>
            <h2>Edit Resume: {editingResume.title}</h2>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                updateResume();
              }}
            >
              <div>
                <label>
                  Title:
                  <input
                    type="text"
                    value={newTitle}
                    onChange={(e) => setNewTitle(e.target.value)}
                  />
                </label>
              </div>
              <div>
                <label>
                  Description:
                  <input
                    type="text"
                    value={newDescription}
                    onChange={(e) => setNewDescription(e.target.value)}
                  />
                </label>
              </div>
              <div>
                <label>
                  Date:
                  <input
                    type="date"
                    value={newDate}
                    onChange={(e) => setNewDate(e.target.value)}
                  />
                </label>
              </div>
              <div>
                <label>
                  PDF URL:
                  <input
                    type="text"
                    value={newPdfUrl}
                    onChange={(e) => setNewPdfUrl(e.target.value)}
                  />
                </label>
              </div>
              <button type="submit">Update Resume</button>
            </form>
          </div>
        )}
        {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}
      </div>
    </div>
  );
}

export default Resumes;
