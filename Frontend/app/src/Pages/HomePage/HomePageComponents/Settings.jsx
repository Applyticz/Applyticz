import React, { useState, useEffect } from 'react';
import useAuth from "../../../utils";
import "./Settings.css";

function Settings() {
  const { authTokens } = useAuth();
  const [settings, setSettings] = useState({
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
        setSettings(data);
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
