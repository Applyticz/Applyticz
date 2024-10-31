import React, { useState, useEffect } from 'react';
import useAuth from "../../utils";
import "./DashboardPage.css";
import { Show } from '@chakra-ui/react';

function Dashboard() {
  const { authTokens } = useAuth();
  const [dashboardData, setDashboardData] = useState({
    totalApplications: 0,
    totalResumes: 0,
    recentApplications: [],
    recentResumes: []
  });
  const [theme, setTheme] = useState('light');
  const [error, setError] = useState('');
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetchTheme();
    fetchDashboardData();
    fetchUpcomingEvents();
  }, []);


  const fetchDashboardData = async () => {
    try {
      const response = await fetch("http://localhost:8000/dashboard/get_data", {
        headers: {
          "Authorization": `Bearer ${authTokens}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setDashboardData(data);
      } else {
        throw new Error('Failed to fetch dashboard data');
      }
    } catch (err) {
      setError('Error fetching dashboard data');
    }
  };

  const fetchUpcomingEvents = async () => {
    try {
      const response = await fetch(`http://localhost:8000/outlook_api/get-events`, {
        headers: {
          "accept": "application/json", 
          "Authorization": `Bearer ${authTokens}`
        }
      })
      if (response.ok) {
        const data = await response.json();
        setEvents(data.value);
      } else {
        throw new Error('Failed to fetch events');
      }
    }
    catch (err) {
      setError('Error fetching events');
  }
  };

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
    <div className="dashboard-container">
      <h2 style={{ textAlign: 'left'}}>Dashboard</h2>
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
                <button className="details-button" onClick={() => navigate(`/applications/${app.id}`)}>View Details</button>
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
                <div>Uploaded: {new Date(resume.date).toLocaleDateString()}</div>
                <div>Last Updated: {new Date(resume.modified_date).toLocaleDateString()}</div>
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
                <div>Attendees: {event.attendees[0].emailAddress.name}</div>
                <div>Start: {new Date(event.start.dateTime).toLocaleString()}</div>
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
