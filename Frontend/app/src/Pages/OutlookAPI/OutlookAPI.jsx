import React, { useState, useEffect } from "react";

const OutlookApi = () => {
  const [userEmail, setUserEmail] = useState("");
  const [search, setSearch] = useState("");
  const [messages, setMessages] = useState([]);
  const [errorMessage, setErrorMessage] = useState("");
  const [lastRefreshTime, setLastRefreshTime] = useState(
    localStorage.getItem("lastRefreshTime") || ""
  );

  const getCurrentTime = () => {
    const date = new Date();
    return date.toISOString().split(".")[0] + "Z";
  };

  const saveLastRefreshTime = (time) => {
    setLastRefreshTime(time);
    localStorage.setItem("lastRefreshTime", time);
  };

  const createApplicationFromEmail = async (parsedApplication) => {
    try {
      const response = await fetch(
        "http://localhost:8000/application/create_application",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
          body: JSON.stringify(parsedApplication),
        }
      );

      if (response.ok) {
        const data = await response.json();
        console.log("Application created successfully:", data);
      } else {
        const errorData = await response.json();
        console.error(
          "Failed to create application:",
          errorData.detail || "Unknown error"
        );
      }
    } catch (error) {
      console.error("Error creating application:", error);
    }
  };

  const fetchUserEmail = async () => {
    try {
      const response = await fetch("http://localhost:8000/auth/get_account", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setUserEmail(data.email);
      } else {
        const errorData = await response.json();
        console.error(
          "Failed to fetch user:",
          errorData.detail || "Unknown error"
        );
      }
    } catch (error) {
      console.error("Error fetching user details:", error);
    }
  };

  const fetchAndCreateApplicationsBySearch = async () => {
    try {
      if (!userEmail) {
        setErrorMessage("User email not found.");
        return;
      }

      const response = await fetch(
        `http://localhost:8000/outlook_api/get-user-messages-by-phrase?email=${userEmail}&phrase=${search}`,
        {
          headers: {
            accept: "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
          },
        }
      );

      if (response.ok) {
        const emails = await response.json();
        setMessages(emails);
        console.log("Fetched messages:", emails);

        if (emails.length === 0) {
          setErrorMessage("No new messages found.");
          return;
        }

        emails.forEach((msg) => {
          if (msg && Object.keys(msg).length > 0) {
            const parsedApplication = (msg);
            createApplicationFromEmail(parsedApplication);
          }
        });
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.detail || "Failed to fetch messages.");
      }
    } catch (error) {
      console.error("Error fetching messages:", error);
      setErrorMessage("An error occurred. Please try again.");
    }
  };

  /* const fetchAndCreateApplicationBySearchAndDate = async () => {
    try {
      if (!userEmail) {
        setErrorMessage("User email not found.");
        return;
      }

      const response = await fetch(
        `http://localhost:8000/outlook_api/`
      )
  }
      */

  const parseApplicationData = (msg) => {
    return {
      company: msg.company || "Unknown",
      position: msg.position || "Unknown",
      location: msg.location || "Unknown",
      status: msg.status || "Unknown",
      salary: msg.salary || "Unknown",
      job_description: msg.job_description || "Not provided",
      notes: msg.notes || "",
    };
  };

  useEffect(() => {
    fetchUserEmail();
  }, []);

  return (
    <div className="outlook-api-container">
      <h2>Fetch Outlook Messages and Create Applications</h2>

      <input
        type="text"
        placeholder="Search phrase"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <button onClick={fetchAndCreateApplicationsBySearch}>
        Fetch and Create Applications by Search
      </button>

      {errorMessage && <p className="error-message">{errorMessage}</p>}

      {messages.length > 0 && (
        <div className="messages-list">
          <h3>Fetched Messages:</h3>
          <ul>
            {messages.map((msg, index) => (
              <li key={index}>
                <strong>Subject:</strong> {msg.subject} <br />
                <strong>From:</strong>{" "}
                {typeof msg.from === "object"
                  ? msg.from?.emailAddress?.address || "Unknown"
                  : msg.from || "Unknown"}{" "}
                <br />
                <strong>Received At:</strong> {msg.receivedDateTime} <br />
                <strong>Preview:</strong> {msg.bodyPreview} <br />
                <strong>Body:</strong> {msg.body}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default OutlookApi;
