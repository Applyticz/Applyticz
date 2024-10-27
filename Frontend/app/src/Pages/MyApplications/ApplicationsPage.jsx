import React, { useState, useEffect } from 'react';

//Chakra
import { ChakraProvider } from '@chakra-ui/react'
import {Modal, ModalContent, ModalHeader, ModalFooter, ModalBody} from '@chakra-ui/react'
import { Button } from '@chakra-ui/react'
import { ArrowForwardIcon } from '@chakra-ui/icons'
import { Input, Textarea, FormControl, FormLabel, Grid, GridItem } from '@chakra-ui/react';

import useAuth from "../../utils";
import "./ApplicationsPage.css";
import "../../App.css";
import Tabs from './Tabbing.jsx';

function Applications() {
  const { authTokens } = useAuth();
  const [applications, setApplications] = useState([]);
  const [error, setError] = useState('');
  const [theme, setTheme] = useState('light');

  

  //Create Application Dialogue Box
  const [creatingApplication, setCreatingApplication] = useState(false);
 





  //Old STuff
  const [isCreating, setIsCreating] = useState(false);  
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    company: '',
    position: '',
    status: '',
    applied_date: '',
    notes: ''
  });
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


  useEffect(() => {
    fetchApplications();
    fetchTheme();
  }, []);
  const fetchTheme = async () => {
    try {
      const response = await fetch("http://localhost:8000/settings/get_settings", {
        headers: {
          "Authorization": `Bearer ${authTokens}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setTheme(data.theme || 'light');
      } else {
        throw new Error('Failed to fetch theme');
      }
    } catch (err) {
      setError('Error fetching theme');
    }
  };
  useEffect(() => {
    // Apply the theme by toggling class on the root element
    const root = document.documentElement;
    root.classList.remove('light', 'dark');
    root.classList.add(theme);
  }, [theme]);


  return (
    <div className="applications-container">
      <h2>My Applications</h2>

     
      {/* <button onClick={() => setIsCreating(true)} className="create">
        old button
      </button> */}

      



      
      
      <ChakraProvider>
        <Button colorScheme='gray'>Pull From Email</Button> 
        <Button colorScheme='gray' onClick={() => setCreatingApplication(true)}>New Application</Button>
       
        <Modal isOpen={creatingApplication} onClose={() => setCreatingApplication(false)}>
          <ModalContent>

            <ModalHeader>Create Application</ModalHeader>
            <form onSubmit={(e) => { e.preventDefault(); handleCreate(); setCreatingApplication(false);}}>
              <ModalBody>

                <Grid templateColumns="repeat(2, 1fr)" gap={4}>
                  <GridItem>
                    <FormControl id="company" isRequired>
                      <FormLabel>Company</FormLabel>
                      <Input
                        type="text"
                        name="company"
                        value={formData.company}
                        onChange={(e) => setFormData(prev => ({ ...prev, company: e.target.value }))}
                        placeholder="Company"
                      />
                    </FormControl>
                  </GridItem>

                  <GridItem>
                    <FormControl id="position" isRequired>
                      <FormLabel>Position</FormLabel>
                      <Input
                        type="text"
                        name="position"
                        value={formData.position}
                        onChange={(e) => setFormData(prev => ({ ...prev, position: e.target.value }))}
                        placeholder="Position"
                      />
                    </FormControl>
                  </GridItem>

                  <GridItem>
                    <FormControl id="location" isRequired>
                      <FormLabel>Location</FormLabel>
                      <Input
                        type="text"
                        name="location"
                        value={formData.location}
                        onChange={(e) => setFormData(prev => ({ ...prev, location: e.target.value }))}
                        placeholder="Location"
                      />
                    </FormControl>
                  </GridItem>
                  
                  <GridItem>
                    <FormControl id="salary" isRequired>
                      <FormLabel>Salary</FormLabel>
                      <Input
                        type="text"
                        name="salary"
                        value={formData.salary}
                        onChange={(e) => setFormData(prev => ({ ...prev, salary: e.target.value }))}
                        placeholder="Salary"
                      />
                    </FormControl>
                  </GridItem>

                  <GridItem>
                    <FormControl id="status" isRequired>
                      <FormLabel>Status</FormLabel>
                      <Input
                        type="text"
                        name="status"
                        value={formData.status}
                        onChange={(e) => setFormData(prev => ({ ...prev, status: e.target.value }))}
                        placeholder="Status"
                      />
                    </FormControl>
                  </GridItem>

                  <GridItem colSpan={2}>
                    <FormControl id="job_description">
                      <FormLabel>Job Description</FormLabel>
                      <Textarea
                        name="job_description"
                        value={formData.job_description}
                        onChange={(e) => setFormData(prev => ({ ...prev, job_description: e.target.value }))}
                        placeholder="Job Description"
                      />
                    </FormControl>
                  </GridItem>

                  <GridItem colSpan={2}>
                    <FormControl id="notes">
                      <FormLabel>Notes</FormLabel>
                      <Textarea
                        name="notes"
                        value={formData.notes}
                        onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
                        placeholder="Notes"
                      />
                    </FormControl>
                  </GridItem>
                </Grid>
              </ModalBody>

              <ModalFooter>
                <Button colorScheme='red' mr={3} onClick={() => setCreatingApplication(false)}>Cancel</Button>
                <Button colorScheme='gray' type="submit" rightIcon={<ArrowForwardIcon />}>Create</Button>
              </ModalFooter>
            </form>
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