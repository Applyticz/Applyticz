import React, { useState, useEffect } from "react";
import useAuth from "../../utils";
import "./DashboardPage.css";
import { Show, Modal, ModalOverlay, ModalContent, ModalHeader, ModalBody, ModalCloseButton, Button, ModalFooter } from "@chakra-ui/react";
import { BellIcon } from "@chakra-ui/icons";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const { authTokens } = useAuth();
  const navigate = useNavigate();
  const [dashboardData, setDashboardData] = useState({
    totalApplications: 0,
    totalResumes: 0,
    recentApplications: [],
    recentResumes: [],
  });
  const [theme, setTheme] = useState("light");
  const [error, setError] = useState("");
  const [events, setEvents] = useState([]);
  const [selectedApplication, setSelectedApplication] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [notification, setNotification] = useState("");
  const [newApplications, setNewApplications] = useState([]);

  useEffect(() => {
    fetchTheme();
    fetchDashboardData();
    fetchUpcomingEvents();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await fetch("http://localhost:8000/dashboard/get_data", {
        headers: {
          Authorization: `Bearer ${authTokens}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        setDashboardData(data);
        setNewApplications(data.recentApplications);
        setNotification("New applications or emails have been populated. Please review!");
      } else {
        throw new Error("Failed to fetch dashboard data");
      }
    } catch (err) {
      setError("Error fetching dashboard data");
    }
  };

  const fetchUpcomingEvents = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/outlook_api/get-events`,
        {
          headers: {
            accept: "application/json",
            Authorization: `Bearer ${authTokens}`,
          },
        }
      );
      if (response.ok) {
        const data = await response.json();
        setEvents(data.value);
        setNotification("New events have been fetched. Please check!");
      } else {
        throw new Error("Failed to fetch events");
      }
    } catch (err) {
      setError("Please link your Outlook account to view events");
    }
  };

  const fetchTheme = async () => {
    try {
      const response = await fetch(
        "http://localhost:8000/settings/get_settings",
        {
          headers: {
            Authorization: `Bearer ${authTokens}`,
          },
        }
      );
      if (response.ok) {
        const data = await response.json();
        setTheme(data.theme || "light");
      } else {
        throw new Error("Failed to fetch theme");
      }
    } catch (err) {
      setError("Error fetching theme");
    }
  };

  const getApplication = async (id) => {
    try {
      const response = await fetch(
        `http://localhost:8000/application/get_application/${id}`,
        {
          headers: {
            Authorization: `Bearer ${authTokens}`,
          },
        }
      );
      if (response.ok) {
        const data = await response.json();
        setSelectedApplication(data);
        setIsModalOpen(true);
      } else {
        throw new Error("Failed to fetch application data");
      }
    } catch (err) {
      setError("Error fetching application data");
    }
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setSelectedApplication(null);
  };

  useEffect(() => {
    // Apply the theme by toggling class on the root element
    const root = document.documentElement;
    root.classList.remove("light", "dark");
    root.classList.add(theme);
  }, [theme]);

  const handleBellClick = () => {
    setIsModalOpen(true);
  };

  const handleReviewComplete = (applicationId) => {
    setNewApplications((prev) => prev.filter(app => app.id !== applicationId));
  };

  const handleRedirectToApplications = () => {
    navigate("/applications");
  };

  return (
    <div className="dashboard-container">
      <h2 style={{ textAlign: "left" }}>Dashboard</h2>
      {notification && (
        <div className="notification" onClick={handleBellClick}>
          <BellIcon />
          <span>{notification}</span>
        </div>
      )}
      <Modal isOpen={isModalOpen} onClose={closeModal}>
        <ModalOverlay />
        <ModalContent
          backgroundColor="white"
          boxShadow="lg"
          borderRadius="md"
          p={4}
          maxWidth="600px" // adjust width as needed
        >
          <ModalHeader>Application Details</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            {selectedApplication && (
              <div>
                <p>
                  <strong>Company:</strong> {selectedApplication.company}
                </p>
                <p>
                  <strong>Position:</strong> {selectedApplication.position}
                </p>
                <p>
                  <strong>Status:</strong> {selectedApplication.status}
                </p>
                <p>
                  <strong>Applied Date:</strong>{" "}
                  {selectedApplication.applied_date}
                </p>
                <p>
                  <strong>Location:</strong> {selectedApplication.location}
                </p>
                <p>
                  <strong>Salary:</strong> {selectedApplication.salary}
                </p>
                <p>
                  <strong>Last Update:</strong>{" "}
                  {selectedApplication.last_update}
                </p>
                <p>
                  <strong>Interview Dates:</strong>{" "}
                  {selectedApplication.interview_dates || "N/A"}
                </p>
                <p>
                  <strong>Interview Notes:</strong>{" "}
                  {selectedApplication.interview_notes || "N/A"}
                </p>
                <p>
                  <strong>Notes:</strong> {selectedApplication.notes || "N/A"}
                </p>
                <div className="modal-navigation">
                  <Button colorScheme="blue" mr={3} onClick={handleRedirectToApplications}>
                    Go to Applications Page
                  </Button>
                  <Button colorScheme="green" onClick={() => handleReviewComplete(selectedApplication.id)}>
                    Review Finished
                  </Button>
                </div>
              </div>
            )}
          </ModalBody>
        </ModalContent>
      </Modal>
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>New Applications</ModalHeader>
          <ModalBody>
            {newApplications.length > 0 ? (
              <ul>
                {newApplications.map((app) => (
                  <li key={app.id}>
                    {app.company} - {app.position}
                    <Button 
                      colorScheme="blue" 
                      onClick={() => navigate("/applications")}
                      ml={2}
                    >
                      View Details
                    </Button>
                    <Button 
                      colorScheme="green" 
                      onClick={() => handleReviewComplete(app.id)} 
                      ml={2}
                    >
                      Review Finished
                    </Button>
                  </li>
                ))}
              </ul>
            ) : (
              <p>No new applications to review.</p>
            )}
          </ModalBody>
          <ModalFooter>
            <Button colorScheme="red" onClick={() => setIsModalOpen(false)}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
      <div className="dashboard-summary">
        <div className="summary-card">
          <h3>Total Applications</h3>
          <p>{dashboardData.totalApplications}</p>
        </div>
        <div className="summary-card">
          <h3>Total Resumes</h3>
          <p>{dashboardData.totalResumes}</p>
        </div>
      </div>
      <div className="activity-section">
        <h3>Recent Applications</h3>
        <ul className="activity-list">
          {dashboardData.recentApplications.map((app, index) => (
            <li key={index} className="activity-item">
              <div className="application-info">
                {app.company} - {app.position} ({app.status})
                <button
                  className="details-button"
                  onClick={() => getApplication(app.id)}
                >
                  View Details
                </button>
              </div>
            </li>
          ))}
        </ul>
      </div>
      <div className="activity-section">
        <h3>Recent Resumes</h3>
        <ul className="activity-list">
          {dashboardData.recentResumes.map((resume, index) => (
            <li key={index} className="activity-item">
              <div>
                <strong>{resume.title}</strong>
                <div>
                  Uploaded: {new Date(resume.date).toLocaleDateString()}
                </div>
                <div>
                  Last Updated:{" "}
                  {new Date(resume.modified_date).toLocaleDateString()}
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
      <div className="activity-section">
        <h3>Upcoming Events</h3>
        <ul className="activity-list">
          {events.map((event, index) => (
            <li key={index} className="activity-item">
              <div>
                <strong>{event.subject}</strong>
                <div>
                  Attendees: {event.attendees && event.attendees.length > 0 ? event.attendees[0].emailAddress.name : "No attendees"}
                </div>
                <div>
                  Start: {new Date(event.start.dateTime).toLocaleString()}
                </div>
                <div>End: {new Date(event.end.dateTime).toLocaleString()}</div>
              </div>
            </li>
          ))}
        </ul>
      </div>
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default Dashboard;
