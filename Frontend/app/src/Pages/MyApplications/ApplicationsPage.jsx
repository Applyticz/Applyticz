import React, { useState, useEffect } from 'react';

//Chakra
import { ChakraProvider } from '@chakra-ui/react'
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
} from '@chakra-ui/react'
import { Button, ButtonGroup } from '@chakra-ui/react'
import { ArrowForwardIcon } from '@chakra-ui/icons'
import { AddIcon } from '@chakra-ui/icons'

import useAuth from "../../utils";
import "./ApplicationsPage.css";
import "../../App.css";
import Tabs from './Tabbing.jsx';

function Applications() {
  const { authTokens } = useAuth();
  const [applications, setApplications] = useState([]);
  const [error, setError] = useState('');

  //Remove When modal complete
  const [isCreating, setIsCreating] = useState(false);  

  //Modal
  const [createModal, setCreateModal] = useState(false);
  const openModal_Create = () => setCreateModal(true);
  const closeModal_Create = () => setCreateModal(false);

  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    company: '',
    position: '',
    status: '',
    applied_date: '',
    notes: ''
  });
  useEffect(() => {
    fetchApplications();
  }, []);


  const fetchApplications = async () => {
    try {
      const response = await fetch("http://localhost:8000/application/get_applications", {
        headers: {
          "Authorization": `Bearer ${authTokens}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setApplications(data);
      } else {
        throw new Error('Failed to fetch applications');
      }
    } catch (err) {
      setError('Error fetching applications');
    }
  };
  const handleInputChange = (e, applicationId) => {
    const { name, value } = e.target;
    setApplications(prevApplications => prevApplications.map(app => 
      app.id === applicationId ? { ...app, [name]: value } : app
    ));
  };
  const handleSubmit = async (applicationId) => {
    try {
      const updatedApplication = applications.find(app => app.id === applicationId);
      const response = await fetch(`http://localhost:8000/application/update_application`, {
        method: 'PUT',
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${authTokens}`
        },
        body: JSON.stringify(updatedApplication)
      });

      if (response.ok) {
        setEditingId(null);
        fetchApplications();
      } else {
        throw new Error('Failed to update application');
      }
    } catch (err) {
      setError(err.message);
    }
  };
  const handleCreate = async () => {
    try {
      const response = await fetch("http://localhost:8000/application/create_application", {
        method: 'POST',
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${authTokens}`
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        fetchApplications();
        setIsCreating(false);
        setFormData({ company: '', position: '', location: '', status: '', applied_date: '', last_update: '', salary: '', job_description: '', notes: '' });
      } else {
        throw new Error('Failed to create application');
      }
    } catch (err) {
      setError(err.message);
    }
  };
  const handleDelete = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/application/delete_application?id=${id}`, {
        method: 'DELETE',
        headers: {
          "Authorization": `Bearer ${authTokens}`
        }
      });

      if (response.ok) {
        fetchApplications();
      } else {
        throw new Error('Failed to delete application');
      }
    } catch (err) {
      setError('Error deleting application');
    }
  };


  return (
    <div className="applications-container">
      <h2>My Applications (fix styling)</h2>

      {/* Have it be a plus sign to right, then have it bring up a dialogue*/}
      <button onClick={() => setIsCreating(true)} className="create">
        old button
      </button>

      {/* Another Button to Pull from email */}



      
      
      <ChakraProvider>
        <Button colorScheme='gray'>Pull From Email (make a refresh symbol inside of 'ALL' tab  Large Button)</Button> 
        {/* Maybe put this inside All Tab? */}
        <Button colorScheme='gray' onClick={openModal_Create}>New Application</Button>
       
        {/* When pulling from email, make it so you can bring up a dialogue maybe of New Applications, new Rejections, new Responses, etc... and update them Into List */}
        {/* Upon Pulling from email it notices anything that is not in your current applications and updates gives you a breakdown of what to add etc*/}


        <Modal isOpen={createModal} onClose={closeModal_Create}>
          <ModalContent>

            <ModalHeader>Create Application</ModalHeader>
      
            <ModalBody>
             Create Application Form here
            </ModalBody>

            <ModalFooter>
              <Button colorScheme='red' mr={3} onClick={closeModal_Create}>Cancel</Button>
              <Button colorScheme='gray' rightIcon={<ArrowForwardIcon />}>Create</Button>
            </ModalFooter>

          </ModalContent>
        </Modal>
      </ChakraProvider>
      

       {/* Tabs --> Figure out how to keep rest of styling correct */}
      <Tabs />


      {/* FORM: Add Job Title, Posting  */}

      {isCreating && (
        <form onSubmit={(e) => { e.preventDefault(); handleCreate(); }} className="application-form">
          <input
            type="text"
            name="company"
            value={formData.company}
            onChange={(e) => setFormData(prev => ({ ...prev, company: e.target.value }))}
            placeholder="Company"
            required
          />
          <input
            type="text"
            name="position"
            value={formData.position}
            onChange={(e) => setFormData(prev => ({ ...prev, position: e.target.value }))}
            placeholder="Position"
            required
          />
          <input
            type="text"
            name="location"
            value={formData.location}
            onChange={(e) => setFormData(prev => ({ ...prev, location: e.target.value }))}
            placeholder="Location"
            required
          />
          <input
            type="text"
            name="status"
            value={formData.status}
            onChange={(e) => setFormData(prev => ({ ...prev, status: e.target.value }))}
            placeholder="Status"
            required
          />
          <input
            type="text"
            name="salary"
            value={formData.salary}
            onChange={(e) => setFormData(prev => ({ ...prev, salary: e.target.value }))}
            placeholder="Salary"
            required
          />
          <textarea
            name="job_description"
            value={formData.job_description}
            onChange={(e) => setFormData(prev => ({ ...prev, job_description: e.target.value }))}
            placeholder="Job Description"
          />
          <textarea
            name="notes"
            value={formData.notes}
            onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
            placeholder="Notes"
          />
          <button type="submit">Create</button>
          <button type="button" className="cancel" onClick={() => setIsCreating(false)}>Cancel</button>
        </form>
      )}




      <div className="applications-list">
        {applications.map((application) => (
          <div key={application.id} className="application-item">
            <h3>{application.company} - {application.position}</h3>
            {editingId === application.id ? (
              <div className="application-edit-form">
                <input
                  type="text"
                  name="company"
                  value={application.company}
                  onChange={(e) => handleInputChange(e, application.id)}
                  placeholder="Company"
                  required
                />
                <input
                  type="text"
                  name="position"
                  value={application.position}
                  onChange={(e) => handleInputChange(e, application.id)}
                  placeholder="Position"
                  required
                />
                <input
                  type="text"
                  name="location"
                  value={application.location}
                  onChange={(e) => handleInputChange(e, application.id)}
                  placeholder="Location"
                  required
                />
                <input
                  type="text"
                  name="status"
                  value={application.status}
                  onChange={(e) => handleInputChange(e, application.id)}
                  placeholder="Status"
                  required
                />
                <input
                  type="text"
                  name="salary"
                  value={application.salary}
                  onChange={(e) => handleInputChange(e, application.id)}
                  placeholder="Salary"
                  required
                />
                <textarea
                  name="job_description"
                  value={application.job_description}
                  onChange={(e) => handleInputChange(e, application.id)}
                  placeholder="Job Description"
                />
                <textarea
                  name="notes"
                  value={application.notes}
                  onChange={(e) => handleInputChange(e, application.id)}
                  placeholder="Notes"
                />
                <div className="button-group">
                  <button onClick={() => handleSubmit(application.id)} className="save">Save</button>
                  <button onClick={() => setEditingId(null)} className="cancel">Cancel</button>
                </div>
              </div>
            ) : (
              <div className="application-display">
                <p>Status: {application.status}</p>
                <p>Applied Date: {application.applied_date}</p>
                <p>Last Update: {application.last_update}</p>
                <p>Notes: {application.notes}</p>
                <div className="button-group">
                  <button onClick={() => setEditingId(application.id)} className="edit">Edit</button>
                  <button onClick={() => handleDelete(application.id)} className="delete">Delete</button>
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

export default Applications;
