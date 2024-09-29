import React, { useState, useEffect } from 'react';
import useAuth from "../../../utils";
import "./Resume.css";

function Resumes() {
  const { authTokens } = useAuth();
  const [resumes, setResumes] = useState([]);
  const [error, setError] = useState('');
  const [isCreating, setIsCreating] = useState(false);
  const [editingData, setEditingData] = useState({
    title: '',
    description: '',
    pdf_data: null
  });
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    pdf_data: null
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

  const handleEditInputChange = (e) => {
    const { name, value } = e.target;
    setEditingData(prev => ({ ...prev, [name]: value }));
  };

  const handleEditFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setEditingData(prev => ({ ...prev, pdf_data: file }));
    }
  };

  const handleSubmit = async () => {
    try {
      // Prepare FormData for updating
      const data = new FormData();
      data.append('description', editingData.description);

      if (editingData.pdf_data) {
        data.append('pdf', editingData.pdf_data);
      }

      const response = await fetch(`http://localhost:8000/resume/update_resume?title=${encodeURIComponent(editingData.title)}`, {
        method: 'PUT',
        headers: {
          "Authorization": `Bearer ${authTokens}`
        },
        body: data
      });

      if (response.ok) {
        fetchResumes();
        setEditingData({ title: '', description: '', pdf_data: null });
      } else {
        throw new Error('Failed to update resume');
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleCreate = async () => {
    try {
      const data = new FormData();
      data.append('title', formData.title);
      data.append('description', formData.description);

      if (formData.pdf_data) {
        data.append('pdf', formData.pdf_data);
      }

      const response = await fetch("http://localhost:8000/resume/upload_resume", {
        method: 'POST',
        headers: {
          "Authorization": `Bearer ${authTokens}`
        },
        body: data
      });

      if (response.ok) {
        fetchResumes(); // Refresh the resume list
        setIsCreating(false);
        setFormData({ title: '', description: '', pdf_data: null });
      } else {
        throw new Error('Failed to create resume');
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const handleDelete = async (title) => {
    const confirmed = window.confirm(`Are you sure you want to delete ${title}? This action cannot be undone.`);
    if (confirmed) {
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

  const handleDeleteAll = async () => {
        const confirmed = window.confirm("Are you sure you want to delete all resumes? This action cannot be undone.");
        if (confirmed) {
          try {
            const response = await fetch("http://localhost:8000/resume/delete_all_resumes", {
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
    
      const handleFileUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
          setFormData((prev) => ({ ...prev, pdf_data: file }));
        }
      };
    
      const fetchAndOpenPdf = async (title) => {
        try {
          const response = await fetch(`http://localhost:8000/resume/get_resume_pdf?title=${encodeURIComponent(title)}`, {
            method: 'GET',
            headers: {
              "Authorization": `Bearer ${authTokens}`
            }
          });
    
          if (response.ok) {
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            window.open(url, '_blank', 'noopener,noreferrer');
          } else {
            const errorText = await response.text();
            console.error('Failed to fetch PDF:', response.status, errorText);
          }
        } catch (error) {
          console.error('Error fetching PDF:', error);
        }
      };
    
      return (
        <div>
          <div className="button-bar">
            <h1>My Resumes</h1>
            <button onClick={() => setIsCreating(true)} className="create">Create New Resume</button>
            <button onClick={handleDeleteAll} className="delete-all">Delete All Resumes</button>
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
                type="file"
                accept="application/pdf"
                onChange={handleFileUpload}
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
                {editingData.title === resume.title ? (
                  <div className="resume-edit-form">
                    <textarea
                      name="description"
                      value={editingData.description}
                      onChange={handleEditInputChange}
                      placeholder="Description"
                      required
                    />
                    <input
                      type="file"
                      accept="application/pdf"
                      onChange={handleEditFileUpload}
                    />
                    <div className="button-group">
                      <button onClick={handleSubmit} className="save">Save</button>
                      <button onClick={() => setEditingData({ title: '', description: '', pdf_data: null })} className="cancel">Cancel</button>
                    </div>
                  </div>
                ) : (
                  <div className="resume-display">
                    <p className="description"><b>Description: </b>{resume.description}</p>
                    <p className="date"><b>Date:</b> {resume.date}</p>
                    <p className="modified_date"><b>Modified Date: </b> {resume.modified_date}</p>
                    <button onClick={() => fetchAndOpenPdf(resume.title)} className="pdf-link"> View PDF</button>
                    <div className="button-group">
                      <button onClick={() => setEditingData({ title: resume.title, description: resume.description, pdf_data: null })} className="edit">Edit</button>
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
