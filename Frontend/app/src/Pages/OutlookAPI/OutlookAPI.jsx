import React, { useState, useEffect } from "react";

const OutlookApi = () => {
  const [userEmail, setUserEmail] = useState(""); // To store the user's email fetched from backend
  const [search, setSearch] = useState(""); // To store the search phrase
  const [messages, setMessages] = useState([]); // To store the fetched messages
  const [errorMessage, setErrorMessage] = useState(""); // To store any error message

  // Function to fetch the logged-in user's email from the /user endpoint
  const fetchUserEmail = async () => {
    try {
        const response = await fetch("http://localhost:8000/auth/get_account", {
            method: "GET",
            headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`, // Still using token for auth
            },
        });

        if (response.ok) {
            const data = await response.json();
            console.log("User Details:", data); // Log or use the returned user details
            // set the user email in state to the email fetched from the backend
            setUserEmail(data.email);
            console.log("User Email:", data.email); // Log or use the returned email
        } else {
            const errorData = await response.json();
            console.error("Failed to fetch user:", errorData.detail || "Unknown error");
        }
        } catch (error) {
        console.error("Error fetching user details:", error);
        }
    };

  // Function to fetch user messages
  const fetchUserMessages = async () => {
    try {
      if (!userEmail) {
        setErrorMessage("User email not found.");
        return;
      }

      const response = await fetch(
        `http://localhost:8000/outlook_api/get-user-messages?email=${userEmail}`
      );
        console.log("User Email for fetch:", userEmail);
      if (response.ok) {
        const data = await response.json();
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
        `http://localhost:8000/outlook_api/get-user-messages-by-phrase?email=${userEmail}&phrase=${search}`
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

  // Fetch user email when the component mounts
  useEffect(() => {
    fetchUserEmail();
  }, []);

  return (
    <div className="outlook-api-container">
      <h2>Fetch Outlook Messages</h2>

      <div className="form-group">
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search messages"
        />
      </div>

      <button onClick={fetchUserMessages}>Fetch Messages</button>
      <button onClick={fetchMessagesByPhrase}>Search Messages</button>

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
                <strong>Preview:</strong> {msg.bodyPreview}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default OutlookApi;
