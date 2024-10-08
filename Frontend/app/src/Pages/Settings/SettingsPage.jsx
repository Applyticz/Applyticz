import React, { useState, useEffect } from 'react';
import useAuth from "../../utils";
import "./SettingsPage.css";

function Settings() {
  const { authTokens } = useAuth();
  const [settings, setSettings] = useState({
    first_name: '',
    last_name: '',
    university: '',
    email: '',
    age: '',
    gender: '',
    desired_role: '',
    theme: 'light',
    notification_preferences: ''
  });
  const [error, setError] = useState('');

  useEffect(() => {
    fetchSettings();
  }, []);

  const fetchSettings = async () => {
    try {
      const response = await fetch("http://localhost:8000/settings/get_settings", {
        headers: {
          "Authorization": `Bearer ${authTokens}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setSettings({
          first_name: data.first_name || '',
          last_name: data.last_name || '',
          university: data.university || '',
          email: data.email || '',
          age: data.age || '',
          gender: data.gender || '',
          desired_role: data.desired_role || '',
          theme: data.theme || 'light',
          notification_preferences: data.notification_preferences || ''
        });
      } else {
        throw new Error('Failed to fetch settings');
      }
    } catch (err) {
      setError('Error fetching settings');
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSettings(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8000/settings/update_settings", {
        method: 'PUT',
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${authTokens}`
        },
        body: JSON.stringify(settings)
      });

      if (response.ok) {
        // Optionally, you can show a success message here
      } else {
        throw new Error('Failed to update settings');
      }
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="settings-container">
      <h2>User Settings</h2>
      <form onSubmit={handleSubmit} className="settings-form">
        <label>
          First Name:
          <input
            type="text"
            name="first_name"
            value={settings.first_name}
            onChange={handleInputChange}
          />
        </label>
        <label>
          Last Name:
          <input
            type="text"
            name="last_name"
            value={settings.last_name}
            onChange={handleInputChange}
          />
        </label>
        <label>
          University:
          <input
            type="text"
            name="university"
            value={settings.university}
            onChange={handleInputChange}
          />
        </label>
        <label>
          Email:
          <input
            type="email"
            name="email"
            value={settings.email}
            onChange={handleInputChange}
          />
        </label>
        <label>
          Age:
          <input
            type="number"
            name="age"
            value={settings.age}
            onChange={handleInputChange}
          />
        </label>
        <label>
          Gender:
          <input
            type="text"
            name="gender"
            value={settings.gender}
            onChange={handleInputChange}
          />
        </label>
        <label>
          Desired Role:
          <select
            name="desired_role"
            value={settings.desired_role}
            onChange={handleInputChange}
          >
            <option value="">Select a role</option>
            <option value="software_engineer">Software Engineer</option>
            <option value="data_scientist">Data Scientist</option>
            <option value="data_analyst">Data Analyst</option>
            <option value="product_manager">Product Manager</option>
            <option value="ux_designer">UX Designer</option>
          </select>
        </label>
        <label>
          Theme:
          <select
            name="theme"
            value={settings.theme}
            onChange={handleInputChange}
          >
            <option value="light">Light</option>
            <option value="dark">Dark</option>
          </select>
        </label>
        <label>
          Notification Preferences:
          <input
            type="text"
            name="notification_preferences"
            value={settings.notification_preferences}
            onChange={handleInputChange}
            placeholder="Enter notification preferences"
          />
        </label>
        <button type="submit">Save Settings</button>
      </form>
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default Settings;
