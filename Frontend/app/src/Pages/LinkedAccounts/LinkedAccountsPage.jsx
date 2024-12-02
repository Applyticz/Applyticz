import React, { useState, useEffect } from "react";
import useAuth from "../../utils";
import "../../App.css";

// Chakra UI imports
import {
  ChakraProvider,
  Button,
  Modal,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
} from "@chakra-ui/react";

function LinkedAccounts() {
  const { authTokens } = useAuth();
  const [outlookAccounts, setOutlookAccounts] = useState([]);
  const [error, setError] = useState("");
  const [addingNewGmail, setAddingNewGmail] = useState(false);
  const [theme, setTheme] = useState("light");

  // Gmail OAuth URL parameters
  const gmailAuthServer = "https://accounts.google.com/o/oauth2/v2/auth?";
  const clientID =
    "client_id=540720712071-3ki8o3kpog4int741skr5rb817lo2543.apps.googleusercontent.com";
  const redirectURI =
    "&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fgmail_api%2Fcallback";
  const responseType = "&response_type=code";
  const scopes =
    "&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.readonly";

  const redirectToOAuthConsentScreen = () => {
    const gmailAuthenticationLink =
      gmailAuthServer + clientID + redirectURI + responseType + scopes;
    window.location.href = gmailAuthenticationLink;
  };

  const addGmail = () => {
    window.location.href = `http://localhost:8000/gmail_api/login?state=${authTokens}`;
  }
  
  const getGmailAccounts = async () => {
    try {
      const response = await fetch("http://localhost:8000/gmail_api/get-accounts", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${authTokens}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        console.log("Gmail Accounts:", data);
        setGmailAccounts(data.emailAddresses); // Store Gmail accounts in state
      } else {
        const errorData = await response.json();
        setError(errorData.detail || "Failed to get Gmail accounts.");
      }
    } catch (error) {
      console.error("Error:", error);
      setError("An error occurred while fetching Gmail accounts. Please try again.");
    }
  };

  // Outlook Adding & Authentication
  const addOutlook = () => {
    window.location.href = `http://localhost:8000/outlook_api/login?state=${authTokens}`;
  };

  const getOutlookAccounts = async () => {
    try {
      const response = await fetch(
        "http://localhost:8000/outlook_api/get-user",
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${authTokens}`,
          },
        }
      );
      if (response.ok) {
        const data = await response.json();
        // console.log("Outlook Accounts:", data);
        setOutlookAccounts(data.userPrincipalName); // Store accounts in state
      } else {
        const errorData = await response.json();
        setError(errorData.detail || "Failed to get accounts.");
      }
    } catch (error) {
      console.error("Error:", error);
      setError("An error occurred. Please try again.");
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

  useEffect(() => {
    // Apply the theme by toggling class on the root element
    const root = document.documentElement;
    root.classList.remove("light", "dark");
    root.classList.add(theme);
  }, [theme]);

  // Fetch Outlook accounts when component mounts
  useEffect(() => {
    fetchTheme();
    getOutlookAccounts();
    getGmailAccounts();
  }, []);

  return (
    <>
      <h2 style={{ textAlign: "left", fontWeight: "bold" }}>Linked Accounts</h2>
      <ChakraProvider>
        {/* Gmail Section */}
        <h1>Gmail</h1>
        <Button colorScheme="gray" onClick={() => setAddingNewGmail(true)}>
          Link New Account
        </Button>

        {/* Outlook Section */}
        <h1>Outlook</h1>
        <p>{outlookAccounts}</p>
        {/* {error && <p style={{ color: "red" }}>{error}</p>} */}
        <Button colorScheme="gray" onClick={addOutlook}>
          Link New Account
        </Button>

        {/* Gmail Authentication Modal */}
        <Modal isOpen={addingNewGmail} onClose={() => setAddingNewGmail(false)}>
          <ModalContent>
            <ModalHeader>Add Gmail Account</ModalHeader>
            <ModalBody>
              <p>
                To link your Gmail account and enable automatic updates, Google
                authentication is required. By clicking the "Authenticate"
                button below, you will be redirected to their authentication and
                consent screen where you can grant Applyticz read-only access to
                your email. This is entirely optional, and Applyticz can still
                be used manually if you choose not to grant email permissions;
                however, you will not be able to use the automatic update
                features.
              </p>
            </ModalBody>
            <ModalFooter>
              <Button
                colorScheme="red"
                mr={3}
                onClick={() => setAddingNewGmail(false)}
              >
                Cancel
              </Button>
              <Button colorScheme="gray" onClick={addGmail}>
                Authenticate
              </Button>
            </ModalFooter>
          </ModalContent>
        </Modal>
      </ChakraProvider>
    </>
  );
}

export default LinkedAccounts;
