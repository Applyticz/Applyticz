import React, { useState, useEffect } from 'react';
import useAuth from "../../../utils";
import "./Resume.css";

function Resumes() {
  const { authTokens } = useAuth();
  const [resumes, setResumes] = useState([]);
  const [error, setError] = useState('');
  const [isCreating, setIsCreating] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    date: '',
    modified_date: '',
    pdf_url: '',
    pdf_file: ''
  });

  useEffect(() => {
    fetchResumes();
  }, []);

  const fetchResumes = async () => {
    try {
      const response = await fetch("http://localhost:8000/resume/get_resumes", {
        headers: {
          "Authorization": `Bearer ${authTokens}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setResumes(data);
      } else {
        throw new Error('Failed to fetch resumes');
      }
    } catch (err) {
      setError('Error fetching resumes');
    }
  };

  const handleInputChange = (e, resumeTitle) => {
    const { name, value } = e.target;
    setResumes(prevResumes => prevResumes.map(resume => 
      resume.title === resumeTitle ? { ...resume, [name]: value } : resume
    ));
  };

  const handleSubmit = async (resumeTitle) => {
    try {
      const updatedResume = resumes.find(resume => resume.title === resumeTitle);
      const response = await fetch(`http://localhost:8000/resume/update_resume?title=${resumeTitle}`, {
        method: 'PUT',
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${authTokens}`
        },
        body: JSON.stringify(updatedResume)
      });

      if (response.ok) {
        setEditingId(null);
      } else {
        throw new Error('Failed to update resume');
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleCreate = async () => {
    try {
      const response = await fetch("http://localhost:8000/resume/upload_resume", {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${authTokens}`
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        fetchResumes();
        setIsCreating(false);
        setFormData({ title: '', description: '', date: '', modified_date: '', pdf_url: '', pdf_file: '' });
      } else {
        throw new Error('Failed to create resume');
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (title) => {

    const confirmed = window.confirm("Are you sure you want to delete " + title + ". This action cannot be undone.");

    if(confirmed)
    {
      try {
        const response = await fetch(`http://localhost:8000/resume/delete_resume?title=${title}`, {
          method: 'DELETE',
          headers: {
            "Authorization": `Bearer ${authTokens}`
          }
        });
  
        if (response.ok) {
          fetchResumes();
        } else {
          throw new Error('Failed to delete resume');
        }
      } catch (err) {
        setError('Error deleting resume');
      }
    }
  };

  const handleDeleteAll = async (title) => {
    const confirmed = window.confirm("Are you sure you want to delete all resumes? This action cannot be undone.");

    if(confirmed)
    {
      try {
        const response = await fetch(`http://localhost:8000/resume/delete_all_resumes`, {
          method: 'DELETE',
          headers: {
            "Authorization": `Bearer ${authTokens}`
          }
        });
  
        if (response.ok) {
          fetchResumes();
        } else {
          throw new Error('Failed to delete all resumes');
        }
      } catch (err) {
        setError('Error deleting resumes');
      }
    }
  };

  return (
    <div>
      <div className="button-bar">

        <h1>My Resumes</h1>

        <button onClick={() => setIsCreating(true)} className="create">
          Create New Resume
        </button>

        <button onClick={handleDeleteAll} className="delete-all">
          Delete All Resumes
        </button>

      </div>
      
      {isCreating && (
        <form onSubmit={(e) => { e.preventDefault(); handleCreate(); }} className="resume-form">
          <input
            type="text"
            name="title"
            value={formData.title}
            onChange={(e) => setFormData(prev => ({ ...prev, title: e.target.value }))}
            placeholder="Title"
            required
          />
          <textarea
            name="description"
            value={formData.description}
            onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
            placeholder="Description"
            required
          />
          <input
            type="text"
            name="pdf_url"
            value={formData.pdf_url}
            onChange={(e) => setFormData(prev => ({ ...prev, pdf_url: e.target.value }))}
            placeholder="PDF URL"
            required
          />
          <div className="button-group">
            <button type="submit">Create</button>
            <button type="button" onClick={() => setIsCreating(false)} className="cancel">Cancel</button>
          </div>
        </form>
      )}

      <div className="resume-container">
        {resumes.map((resume) => (
          <div key={resume.title} className="resume-item">
            <h3>{resume.title}</h3>
            {editingId === resume.title ? (
              <div className="resume-edit-form">
                <textarea
                  name="description"
                  value={resume.description}
                  onChange={(e) => handleInputChange(e, resume.title)}
                  placeholder="Description"
                  required
                />
                <input
                  type="text"
                  name="pdf_url"
                  value={resume.pdf_url}
                  onChange={(e) => handleInputChange(e, resume.title)}
                  placeholder="PDF URL"
                  required
                />
                <div className="button-group">
                  <button onClick={() => handleSubmit(resume.title)} className="save">Save</button>
                  <button onClick={() => setEditingId(null)} className="cancel">Cancel</button>
                </div>
              </div>
            ) : (
              <div className="resume-display">
                <p className="description"><b>Description: </b>{resume.description}</p>
                <p className="date"><b>Date:</b> {resume.date}</p>
                <p className="modified_date"><b>Modified Date: </b>: {resume.modified_date}</p>
                <a href={resume.pdf_url} target="_blank" rel="noopener noreferrer" className="pdf-link">View PDF</a>
                <div className="button-group">
                  <button onClick={() => setEditingId(resume.title)} className="edit">Edit</button>
                  <button onClick={() => handleDelete(resume.title)} className="delete">Delete</button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default Resumes;
