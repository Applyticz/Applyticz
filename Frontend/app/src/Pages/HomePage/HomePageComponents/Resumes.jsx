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
    pdf_url: ''
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
        setFormData({ title: '', description: '', date: '', pdf_url: '' });
      } else {
        throw new Error('Failed to create resume');
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (title) => {
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
  };

  return (
    <div className="resumes-container">
      <h2>My Resumes</h2>
      <button onClick={() => setIsCreating(true)} className="create">
        Create New Resume
      </button>

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
          <input
            type="text"
            name="description"
            value={formData.description}
            onChange={(e) => setFormData(prev => ({ ...prev, description: e.target.value }))}
            placeholder="Description"
            required
          />
          <input
            type="date"
            name="date"
            value={formData.date}
            onChange={(e) => setFormData(prev => ({ ...prev, date: e.target.value }))}
            required
          />
          <input
            type="url"
            name="pdf_url"
            value={formData.pdf_url}
            onChange={(e) => setFormData(prev => ({ ...prev, pdf_url: e.target.value }))}
            placeholder="PDF URL"
            required
          />
          <button type="submit">Create</button>
          <button type="button" onClick={() => setIsCreating(false)}>Cancel</button>
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
                  type="date"
                  name="date"
                  value={resume.date}
                  onChange={(e) => handleInputChange(e, resume.title)}
                  required
                />
                <input
                  type="url"
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
                <p className="description">{resume.description}</p>
                <p className="date">Date: {resume.date}</p>
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
