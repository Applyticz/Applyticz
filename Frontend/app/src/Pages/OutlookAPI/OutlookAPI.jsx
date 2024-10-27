import React, { useState, useEffect } from "react";



const OutlookApi = () => {
  const [userEmail, setUserEmail] = useState(""); // To store the user's email fetched from backend
  const [search, setSearch] = useState(""); // To store the search phrase
  const [messages, setMessages] = useState([]); // To store the fetched messages
  const [errorMessage, setErrorMessage] = useState(""); // To store any error message

  // Function to parse email and create a new application
  const createApplicationFromEmail = async (msg) => {
    const parsedApplication = parseApplicationData(msg);

    // Call the create_application API to save the parsed application
    try {
      const response = await fetch("http://localhost:8000/application/create_application", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify({
          company: parsedApplication.company,
          position: parsedApplication.position,
          location: parsedApplication.location,
          status: parsedApplication.status,
          salary: parsedApplication.salary,
          job_description: parsedApplication.job_description,
          notes: parsedApplication.notes,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        console.log("Application created successfully:", data);
      } else {
        const errorData = await response.json();
        console.error("Failed to create application:", errorData.detail || "Unknown error");
      }
    } catch (error) {
      console.error("Error creating application:", error);
    }
  };

  // Function to fetch the logged-in user's email from the /user endpoint
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
        console.error("Failed to fetch user:", errorData.detail || "Unknown error");
      }
    } catch (error) {
      console.error("Error fetching user details:", error);
    }
  };

  // Fetch messages and then create applications based on the parsed data
  const fetchAndCreateApplications = async () => {
    try {
      if (!userEmail) {
        setErrorMessage("User email not found.");
        return;
      }

      const response = await fetch(
        `http://localhost:8000/outlook_api/get-user-messages?email=${userEmail}`, {
        headers: {
          "accept": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
        }
      }
      );

      if (response.ok) {
        const data = await response.json();
        setMessages(data.value);
        console.log("Messages Data:", data); // Log or use the returned messages

        // Parse each message and create an application
        data.value.forEach((msg) => {
          const parsedApplication = parseApplicationData(msg);
          createApplicationFromEmail(msg);
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

  // Fetch messages based on phrases in the email body and then create applications
  const fetchAndCreateApplicationsBySearch = async () => {
    try {
      if (!userEmail) {
        setErrorMessage("User email not found.");
        return;
      }

      const response = await fetch(
        `http://localhost:8000/outlook_api/get-user-messages-by-phrase?email=${userEmail}&phrase=${search}`, {
        headers: {
          "accept": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
        }
      }
      );

      if (response.ok) {
        const data = await response.json();
        setMessages(data);
        // Parse each message and create an application
        data.forEach((msg) => {
          const parsedApplication = parseApplicationData(msg);
          createApplicationFromEmail(msg);
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

  const parseApplicationData = (msg) => {
  const defaultApplication = {
    company: "Unknown",
    position: "Unknown",
    location: "Unknown",
    status: "Unknown",
    salary: "Unknown",
    job_description: "Not provided",
    notes: "",
  };


  return defaultApplication;
};

const fetchUserMessages = async () => {
    try {
      if (!userEmail) {
        setErrorMessage("User email not found.");
        return;
      }

      const response = await fetch(
        `http://localhost:8000/outlook_api/get-user-messages?email=${userEmail}`, {
        headers: {
          "accept": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
        }
      }
      );
        console.log("User Email for fetch:", userEmail);
      if (response.ok) {
        const data = await response.json();
        console.log("Messages Data:", data); // Log or use the returned messages
        setMessages(data.value); // Assuming the messages are returned directly
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.detail || "Failed to fetch messages.");
      }
    } catch (error) {
      console.error("Error fetching messages:", error);
      setErrorMessage("An error occurred. Please try again.");
    }
  };

  // Function to fetch search messages
  const fetchMessagesByPhrase = async () => {
    try {
      if (!userEmail || !search) {
        setErrorMessage("Please enter a search phrase.");
        return;
      }

      const response = await fetch(
        `http://localhost:8000/outlook_api/get-user-messages-by-phrase?email=${userEmail}&phrase=${search}`, {
        headers: {
          "accept": "application/json",
          "Authorization": `Bearer ${localStorage.getItem("access_token")}`,
        }
      }
      );

      if (response.ok) {
        const data = await response.json();
        setMessages(data); // Assuming the messages are returned directly
      } else {
        const errorData = await response.json();
        setErrorMessage(errorData.detail || "Failed to fetch messages.");
      }
    } catch (error) {
      console.error("Error fetching messages:", error);
      setErrorMessage("An error occurred. Please try again.");
    }
  };


  useEffect(() => {
    fetchUserEmail();
  }, []);

  return (
    <div className="outlook-api-container">
      <h2>Fetch Outlook Messages and Create Applications</h2>

      <button onClick={fetchAndCreateApplications}>Fetch and Create Applications</button>


      <input
        type="text"
        placeholder="Search phrase"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <button onClick={fetchAndCreateApplicationsBySearch}>Fetch and Create Applications by Search</button>

      <button onClick={fetchUserMessages}>Fetch Messages</button>

      <input
        type="text"
        placeholder="Search phrase"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      <button onClick={fetchMessagesByPhrase}>Fetch Messages by Phrase</button>

      {errorMessage && <p className="error-message">{errorMessage}</p>}

      {messages.length > 0 && (
        <div className="messages-list">
          <h3>Fetched Messages:</h3>
          <ul>
            {messages.map((msg, index) => (
              <li key={index}>
                <strong>Subject:</strong> {msg.subject} <br />
                <strong>From:</strong> {typeof msg.from === "object"
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
