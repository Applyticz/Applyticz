import React, { useState, useEffect } from "react";
import mailPic from "../../Images/mailImage.png";

//Chakra
import {
  Card,
  CardHeader,
  CardBody,
  CardFooter,
  Heading,
  Text,
  Image,
  Divider,
  ButtonGroup,
  Alert,
} from "@chakra-ui/react";
import { ChakraProvider, Stack, HStack } from "@chakra-ui/react";
import {
  Modal,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
} from "@chakra-ui/react";
import { Button } from "@chakra-ui/react";
import {
  ArrowForwardIcon,
  ArrowDownIcon,
  ArrowUpIcon,
  AddIcon,
  RepeatIcon,
  EmailIcon,
} from "@chakra-ui/icons";
import {
  Input,
  Textarea,
  FormControl,
  FormLabel,
  Grid,
  GridItem,
  Radio,
  RadioGroup,
  Flex,
} from "@chakra-ui/react";
import { Tabs, TabList, TabPanels, Tab, TabPanel } from "@chakra-ui/react";
import {
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Box,
  IconButton,
  Tooltip,
} from "@chakra-ui/react";

import useAuth from "../../utils";
import "./ApplicationsPage.css";
import "../../App.css";

function Applications() {
  const { authTokens } = useAuth();
  const [error, setError] = useState("");
  const [lastRefreshTime, setlastRefreshTime] = useState("");

  /* Modals */
  const [creatingApplication, setCreatingApplication] = useState(false);
  const handleCreate = async (applicationData, isManualEntry = false) => {
    try {
      const response = await fetch(
        "http://localhost:8000/application/create_application",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authTokens}`,
          },
          body: JSON.stringify({
            ...applicationData,
            applied_date: isManualEntry
              ? new Date().toISOString().split('T')[0]
              : applicationData.applied_date ? new Date(applicationData.applied_date).toISOString().split('T')[0] : "",
            last_update: applicationData.last_update ? new Date(applicationData.last_update).toISOString().split('T')[0] : new Date().toISOString().split('T')[0],
          }),
        }
      );

      if (response.ok) {
        const data = await response.json();
        fetchApplications();
        setApplicationData({
          company: "",
          position: "",
          location: "",
          status: "",
          applied_date: "",
          last_update: "",
          salary: "",
          job_description: "",
          notes: "",
          status_history: [],
          interview_notes: "",
          interview_dates: null,
          interview_round: "",
          is_active_interview: false,
          offer_notes: "",
          offer_interest: 0,
          is_active_offer: false,
          previous_emails: [],
          days_to_update: 0,
        });
        return data;
      } else {
        throw new Error("Failed to create application");
      }
    } catch (err) {
      setError(err.message);
    }
  };


  //Move to Interview/Offer
  const [movingToInterview, setMovingToInterview] = useState(false);
  const [movingToOffer, setMovingToOffer] = useState(false);
  const handleMoveToInterview = async (applicationID, moveToInterviewForm) => {
    // try{

      //Get the application based on id, and now we are going to change the fields we want and send to update
      const currentApplication = {
        ...applicationData, // Sets blank
        ...applications.find((app) => app.id === applicationID), // Overwrites written values
      };

      //Update status, interview_notes, and interview_dates
      currentApplication.status = "Interviewing";
      currentApplication.interview_notes = moveToInterviewForm.interview_notes;
      currentApplication.interview_dates = moveToInterviewForm.interview_dates;

      if (!Array.isArray(currentApplication.status_history)) {
        currentApplication.status_history = [];
    }
  
    currentApplication.status_history = [
        ...currentApplication.status_history,
        currentApplication.status, 
    ];

      const response = await fetch(
        `http://localhost:8000/application/update_application?id=${applicationID}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authTokens}`,
          },
          body: JSON.stringify(currentApplication),
        }
      );


      setMoveToInterviewForm({
        interview_notes: "",
        interview_dates: ""
      })
      if (response.ok) {
        setEditingId(null);
        fetchApplications();
        fetchEmails();
      } else {
        throw new Error("Failed to update application");
      }
    // }catch(err){
    //   console.log("errorrrr thrown")
    //   setError(err.message);
    // }
  }
  const handleMoveToOffer = async(applicationID, moveToOfferForm) => {
    const currentApplication = {
      ...applicationData, // Sets blank
      ...applications.find((app) => app.id === applicationID), // Overwrites written values
    };

    //Update status, interview_notes, and interview_dates
    currentApplication.status = "Offer";
    currentApplication.offer_notes = moveToOfferForm.offer_notes;
    currentApplication.offer_interest = parseInt(moveToOfferForm.offer_interest);
    if (!Array.isArray(currentApplication.status_history)) {
      currentApplication.status_history = [];
  }

  currentApplication.status_history = [
      ...currentApplication.status_history,
      currentApplication.status, 
  ];


    const response = await fetch(
      `http://localhost:8000/application/update_application?id=${applicationID}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${authTokens}`,
        },
        body: JSON.stringify(currentApplication),
      }
    );


    setMoveToOfferForm({
      offer_notes: "",
      offer_interest: ""
    })
    if (response.ok) {
      setEditingId(null);
      fetchApplications();
      fetchEmails();
    } else {
      throw new Error("Failed to update application");
    }
  }


  const [moveToInterviewForm, setMoveToInterviewForm] = useState({
    interview_notes: "",
    interview_dates: ""
  })
  const [moveToOfferForm, setMoveToOfferForm] = useState({
    offer_notes: "", 
    offer_interest: ""
  })
  const updateApplicationStatus = async (applicationID, newStatus) => {
    const currentApplication = {
      ...applicationData, // Sets blank
      ...applications.find((app) => app.id === applicationID), // Overwrites written values
    };

    currentApplication.status = newStatus;

    if (!Array.isArray(currentApplication.status_history)) {
      currentApplication.status_history = [];
  }

  currentApplication.status_history = [
      ...currentApplication.status_history,
      currentApplication.status, 
  ];

    const response = await fetch(
      `http://localhost:8000/application/update_application?id=${applicationID}`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${authTokens}`,
        },
        body: JSON.stringify(currentApplication),
      }
    );

    if (response.ok) {
      setEditingId(null);
      fetchApplications();
      fetchEmails();
    } else {
      throw new Error("Failed to update application");
    }
  }


  const [applicationData, setApplicationData] = useState({
    company: "",
    position: "",
    status: "",
    applied_date: "",
    last_update: "",
    notes: "",
    location: "",
    salary: "",
    job_description: "",
    status_history: [],
    interview_notes: "",
    interview_dates: null,
    interview_round: "",
    is_active_interview: false,
    offer_notes: "",
    offer_interest: 0,
    is_active_offer: false,
    previous_emails: [],
    days_to_update: 0,
  });







  /* Applications List */
  const [applications, setApplications] = useState([]);
  const [emails, setEmail] = useState([]);
  const [editingId, setEditingId] = useState(null);  //This is how the modal gets the id of application we are editing
  useEffect(() => {
    fetchApplications();
    fetchEmails();
    fetchTheme();
  }, []);



  //Handlers
  
  const handleInputChange = (e, applicationId) => {
    const { name, value } = e.target;
    setApplications((prevApplications) =>
      prevApplications.map((app) =>
        app.id === applicationId ? { ...app, [name]: value } : app
      )
    );
  };
  const handleSubmit = async (applicationId) => {
    try {
      const updatedApplication = applications.find(
        (app) => app.id === applicationId
      );
      const response = await fetch(
        `http://localhost:8000/application/update_application`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authTokens}`,
          },
          body: JSON.stringify(updatedApplication),
        }
      );

      if (response.ok) {
        setEditingId(null);
        fetchApplications();
        fetchEmails();
      } else {
        throw new Error("Failed to update application");
      }
    } catch (err) {
      setError(err.message);
    }
  };
  const handleDelete = async (id) => {
    try {
      const response = await fetch(
        `http://localhost:8000/application/delete_application?id=${id}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${authTokens}`,
          },
        }
      );

      if (response.ok) {
        fetchApplications();
      } else {
        throw new Error("Failed to delete application");
      }
    } catch (err) {
      setError("Error deleting application");
    }
  };

  const fetchApplications = async () => {
    try {
      const response = await fetch(
        "http://localhost:8000/application/get_applications",
        {
          headers: {
            Authorization: `Bearer ${authTokens}`,
          },
        }
      );
      if (response.ok) {
        const data = await response.json();
        // // console.log("Applications:", data);
        setApplications(data);
      } else {
        throw new Error("Failed to fetch applications");
      }
    } catch (err) {
      setError("Error fetching applications");
    }
  };
  const fetchEmails = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/email/emails`,
        {
          headers: {
            Authorization: `Bearer ${authTokens}`,
          },
        }
      );
      if (response.ok) {
        const data = await response.json();
        // console.log("EMAILS:", data);
        setEmail(data);
      } else {
        throw new Error("Failed to fetch emails");
      }
    } catch (err) {
      setError("Error fetching emails");
    }
  };
  const [theme, setTheme] = useState("light");
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
  const updatelastRefreshTime = () => {
    const now = new Date();
    const formattedTime = `${now.getUTCFullYear()}-${String(
      now.getUTCMonth() + 1
    ).padStart(2, "0")}-${String(now.getUTCDate()).padStart(2, "0")}T${String(
      now.getUTCHours()
    ).padStart(2, "0")}:${String(now.getUTCMinutes()).padStart(
      2,
      "0"
    )}:${String(now.getUTCSeconds()).padStart(2, "0")}Z`;
    setlastRefreshTime(formattedTime);
    // Update the last refresh time in the database
    updateLastRefreshTime();
  };
  async function updateLastRefreshTime() {
    try {
      const response = await fetch(
        `http://localhost:8000/settings/update_settings`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authTokens}`,
          },
          body: JSON.stringify({
            last_refresh_time: formattedTime,
          }),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to update last refresh time");
      }
    } catch (err) {
      setError(err.message);
    }
  }
  const getNewEmails = async () => {
    try {
      if (!lastRefreshTime) {
        // // console.log("No last update time set");
        await getAllEmails(); // Fetch all emails if no update time is set
      } else {
        const response = await fetch(
          `http://localhost:8000/outlook_api/get-user-messages-by-phrase?phrases=applying&phrases=recruitment&phrases=position&phrases=application&phrases=recruitinglast_refresh_time=${lastRefreshTime}`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${authTokens}`,
            },
          }
        );

        if (response.ok) {
          const data = await response.json();

          // console.log("New emails:", data);

          if (data.message === "No new emails found") {
            setError("No new emails found");
            return;
          }

          // Iterate over each email and create an application
          for (const email of data) {
            // Populate formData with email details
            const formData = {
              company: email.company || "",
              position: email.position || "",
              location: email.location || "",
              status: email.status || "",
              applied_date: email.applied_date || "",
              last_update: email.applied_date || "",
              salary: email.salary || "",
              job_description: email.job_description || "",
              notes: email.notes || "",
              status_history: email.status_history || [],
              interview_notes: email.interview_notes || "",
              interview_dates: email.interview_dates || null,
              interview_round: email.interview_round || "",
              is_active_interview: email.is_active_interview || false,
              offer_notes: email.offer_notes || "",
              offer_interest: email.offer_interest || 0,
              is_active_offer: email.is_active_offer || false,
              previous_emails: email.previous_emails || [],
              days_to_update: email.days_to_update || 0,
            };

            // Pass the populated formData to handleCreate
            await handleCreate(formData); // Pass formData to handleCreate
          }

          updatelastRefreshTime(); // Only update after successful fetch
        } else {
          throw new Error("Failed to get new emails");
        }
      }
    } catch (err) {
      setError(err.message);
    }
  };
  const createEmail = async (emailFormData) => {
    try {
      const response = await fetch("http://localhost:8000/email/create-email", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${authTokens}`,
        },
        body: JSON.stringify({
          ...emailFormData,
        }),
      });

      if (response.ok) {
        // // console.log("Email created successfully");
        fetchEmails();
      } else {
        throw new Error("Failed to create email");
      }
    } catch (err) {
      setError(err.message);
    }
  };
  const getAllEmails = async () => {
    try {
      const response = await fetch(
        `http://localhost:8000/outlook_api/get-user-messages-by-phrase?phrases=applying&phrases=recruitment&phrases=position&phrases=application&phrases=recruiting&phrases=Talent%20Acquisition`,
        {
          method: "GET",
          headers: {
            Authorization: `Bearer ${authTokens}`,
          },
        }
      );

      if (response.ok) {
        const data = await response.json();

        // console.log("All emails:", data);

        // Check if data is an array
        if (!Array.isArray(data)) {
          // Handle the case where data is not an array
          throw new Error(data.message || "Unexpected response format");
        }

        // Handle if no emails are found
        if (data.length === 0) {
          throw new Error("No emails found");
        }

        // Iterate over each email and create an application
        for (const email of data) {
          // Populate formData with application details
          console.log("Email data:", email);
          const formData = {
            company: email.company || "",
            position: email.position || "",
            location: email.location || "",
            status: email.status || "",
            applied_date: email.applied_date || "",
            last_update: email.applied_date || "",
            salary: email.salary || "",
            job_description: email.job_description || "",
            notes: email.notes || "",
            status_history: email.status_history || [],
            interview_notes: email.interview_notes || "",
            interview_dates: email.interview_dates || null,
            interview_round: email.interview_round || "",
            is_active_interview: email.is_active_interview || false,
            offer_notes: email.offer_notes || "",
            offer_interest: email.offer_interest || 0,
            is_active_offer: email.is_active_offer || false,
            previous_emails: email.previous_emails || [],
            days_to_update: email.days_to_update || 0,
          };

          // Pass the populated formData to handleCreate
          const data = await handleCreate(formData); // Pass formData to handleCreate
          
          // console.log("Application data:", data);

          // Create email if it's not a manual entry

            const emailFormData = {
              app: data.application_id,
              subject: email.subject || "",
              sender: email.from || "",
              body: email.body || "",
              body_preview: email.bodyPreview || "",
              applied_date: email.applied_date || "",
              status: email.status || "",
            };
            // console.log("Email data:", emailFormData);
            createEmail({
              ...emailFormData
            });
          }

      } else {
        const errorData = await response.json(); // Get error details from response
        throw new Error(errorData.message || "Failed to get all emails");
      }
    } catch (err) {
      setError(err.message);
      // console.log(err);
    }
  };
  useEffect(() => {
    // Apply the theme by toggling class on the root element
    const root = document.documentElement;
    root.classList.remove("light", "dark");
    root.classList.add(theme);
  }, [theme]);

  return (
    <div className="applications-container">
      <h2 style={{ textAlign: "left", fontWeight: "bold" }}>My Applications</h2>

      <ChakraProvider>
        <Modal isOpen={creatingApplication} onClose={() => setCreatingApplication(false)} size="xl">

          <ModalContent>
            <ModalHeader>New Application</ModalHeader>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleCreate(applicationData, true);
                setCreatingApplication(false);
              }}
            >
              <ModalBody>
                <Grid templateColumns="repeat(2, 1fr)" gap={4}>
                  <GridItem>
                    <FormControl id="company" isRequired>
                      <FormLabel>Company</FormLabel>
                      <Input
                        type="text"
                        name="company"
                        value={applicationData.company}
                        onChange={(e) =>
                          setApplicationData((prev) => ({
                            ...prev,
                            company: e.target.value,
                          }))
                        }
                        placeholder="i.e. Amazon"
                      />
                    </FormControl>
                  </GridItem>

                  <GridItem>
                    <FormControl id="position" isRequired>
                      <FormLabel>Position</FormLabel>
                      <Input
                        type="text"
                        name="position"
                        value={applicationData.position}
                        onChange={(e) =>
                          setApplicationData((prev) => ({
                            ...prev,
                            position: e.target.value,
                          }))
                        }
                        placeholder="i.e. Software Engineer"
                      />
                    </FormControl>
                  </GridItem>

                  <GridItem>
                    <FormControl id="location" isRequired>
                      <FormLabel>Location</FormLabel>
                      <Input
                        type="text"
                        name="location"
                        value={applicationData.location}
                        onChange={(e) =>
                          setApplicationData((prev) => ({
                            ...prev,
                            location: e.target.value,
                          }))
                        }
                        placeholder="i.e. San Francisco, CA"
                      />
                    </FormControl>
                  </GridItem>

                  <GridItem>
                    <FormControl id="salary" isRequired>
                      <FormLabel>Salary</FormLabel>
                      <Input
                        type="text"
                        name="salary"
                        value={applicationData.salary}
                        onChange={(e) =>
                          setApplicationData((prev) => ({
                            ...prev,
                            salary: e.target.value,
                          }))
                        }
                        placeholder="i.e. 115,000"
                      />
                    </FormControl>
                  </GridItem>

                  <GridItem>
                    <FormControl id="status">
                      <FormLabel>Stage</FormLabel>
                      <RadioGroup
                        onChange={(value) =>
                          setApplicationData((prev) => ({ ...prev, status: value }))
                        }
                        value={applicationData.status}
                        defaultValue="Awaiting Response"
                      >
                        <Radio value="Awaiting Response">
                          Awaiting Response
                        </Radio>
                        <Radio value="Positive Response">
                          Positive Response
                        </Radio>
                        <Radio value="Interviewing">Interviewing</Radio>
                        <br></br>
                        <Radio value="Rejected">Rejected</Radio>
                        <br></br>
                        <Radio value="Offer">Offer</Radio>
                      </RadioGroup>
                    </FormControl>
                  </GridItem>

                  <GridItem colSpan={2}>
                    <FormControl id="job_description">
                      <FormLabel>Job Description</FormLabel>
                      <Textarea
                        name="job_description"
                        value={applicationData.job_description}
                        onChange={(e) =>
                          setApplicationData((prev) => ({
                            ...prev,
                            job_description: e.target.value,
                          }))
                        }
                        placeholder="i.e. Expects 2+ years of experience and proficiency in React, NodeJS, and Python"
                      />
                    </FormControl>
                  </GridItem>

                  <GridItem colSpan={2}>
                    <FormControl id="notes">
                      <FormLabel>Notes</FormLabel>
                      <Textarea
                        name="notes"
                        value={applicationData.notes}
                        onChange={(e) =>
                          setApplicationData((prev) => ({
                            ...prev,
                            notes: e.target.value,
                          }))
                        }
                        placeholder="i.e. Anything else you want to add!"
                      />
                    </FormControl>
                  </GridItem>
                </Grid>
              </ModalBody>

              <ModalFooter>
                <Button
                  colorScheme="red"
                  mr={3}
                  onClick={() => setCreatingApplication(false)}
                >
                  Cancel
                </Button>
                <Button
                  colorScheme="gray"
                  type="submit"
                  rightIcon={<ArrowForwardIcon />}
                >
                  Create
                </Button>
              </ModalFooter>
            </form>
          </ModalContent>
        </Modal>

        <Tabs variant="soft-rounded">
          <Flex align="center" mb={4}>
            {/* Tabs */}
            <TabList flex="1">
              <Tab _selected={{ color: "white", bg: "blue.500" }}>All</Tab>
              <Tab _selected={{ color: "white", bg: "yellow.400" }}>
                Awaiting Response
              </Tab>
              <Tab _selected={{ color: "white", bg: "green.400" }}>
                Positive Response
              </Tab>
              <Tab _selected={{ color: "white", bg: "teal.300" }}>
                Interviewing
              </Tab>
              <Tab _selected={{ color: "white", bg: "red.400" }}>Rejected</Tab>
              <Tab _selected={{ color: "white", bg: "purple.300" }}>Offers</Tab>
            </TabList>
            {/* Buttons */}
            <Box ml="auto">
              <Tooltip label="Check for new emails">
                <IconButton
                  colorScheme="gray"
                  icon={<RepeatIcon />}
                  onClick={getNewEmails}
                />
              </Tooltip>
              {/* {error && <p className="error">{error}</p>} */}

              <Tooltip label="Get all emails">
                <IconButton
                  colorScheme="gray"
                  icon={<EmailIcon />}
                  onClick={getAllEmails}
                />
              </Tooltip>
              {/* {error && <p className="error">{error}</p>} */}

              <Tooltip label="Create new application">
                <IconButton
                  colorScheme="gray"
                  icon={<AddIcon />}
                  onClick={() => setCreatingApplication(true)}
                />
              </Tooltip>
            </Box>
          </Flex>

          {/* INDIVIDUAL TABS */}
          <TabPanels mt={-4}>

            {/* ALL */}
            <TabPanel>
              <Flex justify="space-between" align="center">
                <Flex align="center">
                  <Input placeholder="Search" width="300px" />
                  <Button
                    colorScheme="gray"
                    ml={2}
                    rightIcon={<ArrowDownIcon />}
                  >
                    Recent
                  </Button>
                  <Button colorScheme="gray" ml={2} rightIcon={<ArrowUpIcon />}>
                    Oldest
                  </Button>
                </Flex>
                <h1 style={{ textAlign: "right" }}>
                  Total: {applications.length}
                </h1>
              </Flex>
              <br></br>
              <Accordion allowToggle>
                {applications.map((application) => (
                  <AccordionItem key={application.id}>
                    {" "}
                    {/* Iterating through each application (all tab) */}
                    <h2>
                      <AccordionButton
                        _expanded={{ color: "white", bg: "blue.500" }}
                      >
                        <Box as="span" flex="1" textAlign="left">
                          <Box as="span" fontWeight="bold">
                            {application.company || "Company Not Specified"}
                          </Box>
                          ,{" "}
                          <Box as="span" fontStyle="italic">
                            {application.position || "Position Not Specified"}
                          </Box>
                          <br />
                          Applied:{" "}
                          {new Date(
                            application.applied_date
                          ).toLocaleDateString()}
                        </Box>
                        <Box
                          // as="span"
                          // flex="1"
                          // textAlign="right"
                          // borderRadius="full"
                          // border="2px solid"
                          // borderColor="blue.500"
                          // px={3}
                          // py={1}
                          // display="inline-block"
                          // maxW="160px"
                        >
                          {application.status}
                        </Box>
                        <AccordionIcon />
                      </AccordionButton>
                    </h2>
                    <AccordionPanel pb={4}>
                      <p>Location:</p>
                      <p style={{ textIndent: "20px" }}>
                        {application.location}
                      </p>
                      <p>Salary:</p>
                      <p style={{ textIndent: "20px" }}>{application.salary}</p>
                      <p>Job Description:</p>
                      <p style={{ textIndent: "20px" }}>
                        {application.job_description}
                      </p>
                      <p>Notes:</p>
                      <p style={{ textIndent: "20px" }}>{application.notes}</p>
                      <p>Emails:</p>
                      {emails
                        .filter((email) => email.app === application.id)
                        .map((email) => (
                          <div key={email.id} style={{ marginBottom: "10px" }}>
                            <p style={{ fontWeight: "bold" }}>
                              Email Subject: {email.subject || "No Subject"}
                            </p>
                            <p style={{ textIndent: "20px" }}>
                              Email Body: {email.body ||
                                "Email body content not available."}
                            </p>
                          </div>
                        ))}
                      <br />
                      {/* <Button colorScheme="gray">Edit</Button>{" "} */}
                      {/* Make circular */}
                      <Button
                        colorScheme="red"
                        ml={2}
                        onClick={() => handleDelete(application.id)}
                      >
                        Delete
                      </Button>
                    </AccordionPanel>
                  </AccordionItem>
                ))}
              </Accordion>
            </TabPanel>

            {/* TODO: AWAITING RESPONSE */}
            <TabPanel>
              <Flex justify="space-between" align="center">
                <Flex align="center">
                  <Input placeholder="Search" width="300px" />
                  <Button
                    colorScheme="gray"
                    ml={2}
                    rightIcon={<ArrowDownIcon />}
                  >
                    Recent
                  </Button>
                  <Button colorScheme="gray" ml={2} rightIcon={<ArrowUpIcon />}>
                    Oldest
                  </Button>
                </Flex>
                <h1 style={{ textAlign: "right" }}>
                  Total:{" "}
                  {
                    applications.filter(
                      (application) =>
                        application.status === "Awaiting Response"
                    ).length
                  }
                </h1>
              </Flex>
              <br></br>

              {/* List */}
              <Accordion allowToggle>
                {applications
                  .filter(
                    (application) => application.status === "Awaiting Response"
                  )
                  .map((application) => (
                    <AccordionItem key={application.id}>
                      {" "}
                      {/* Iterating through each application (all tab) */}
                      <h2>
                        <AccordionButton
                          _expanded={{ color: "white", bg: "blue.500" }}
                        >
                          <Box as="span" flex="1" textAlign="left">
                            <Box as="span" fontWeight="bold">
                              {application.company || "Company Not Specified"}
                            </Box>
                            ,{" "}
                            <Box as="span" fontStyle="italic">
                              {application.position || "Position Not Specified"}
                            </Box>
                            <br />
                            Applied:{" "}
                            {new Date(
                              application.applied_date
                            ).toLocaleDateString()}
                          </Box>
                          <Box
                            // as="span"
                            // flex="1"
                            // textAlign="right"
                            // borderRadius="full"
                            // border="2px solid"
                            // borderColor="blue.500"
                            // px={3}
                            // py={1}
                            // display="inline-block"
                            // maxW="160px"
                          >
                            {application.status}
                          </Box>
                          <AccordionIcon />
                        </AccordionButton>
                      </h2>
                      <AccordionPanel pb={4}>
                        <p>Location:</p>
                        <p style={{ textIndent: "20px" }}>
                          {application.location || "Location Not Specified"}
                        </p>
                        <p>Salary:</p>
                        <p style={{ textIndent: "20px" }}>
                          {application.salary || "Salary Not Specified"}
                        </p>
                        <p>Job Description:</p>
                        <p style={{ textIndent: "20px" }}>
                          {application.job_description ||
                            "Job Description Not Available"}
                        </p>
                        <p>Notes:</p>
                        <p style={{ textIndent: "20px" }}>
                          {application.notes || "No Notes Available"}
                        </p>
                        <p>Emails:</p>
                        {emails
                          .filter((email) => email.app === application.id)
                          .map((email) => (
                            <div
                              key={email.id}
                              style={{ marginBottom: "10px" }}
                            >
                              <p style={{ fontWeight: "bold" }}>
                                Email Subject: {email.subject || "No Subject"}
                              </p>
                              <p style={{ textIndent: "20px" }}>
                                {email.body ||
                                  "Email body content not available."}
                              </p>
                            </div>
                          ))}
                        {emails.filter((email) => email.app === application.id)
                          .length === 0 && (
                          <p style={{ textIndent: "20px", color: "gray" }}>
                            No emails associated with this application.
                          </p>
                        )}
                        <br />
                        <Button colorScheme="gray" onClick={() => {setMovingToInterview(true); setEditingId(application.id)}}>Move To Interview Stage</Button>{" "}
                        <Button
                          colorScheme="red"
                          ml={2}
                          onClick={() => handleDelete(application.id)}
                        >
                          Delete
                        </Button>
                      </AccordionPanel>
                    </AccordionItem>
                  ))}
              </Accordion>
            </TabPanel>

            {/* POSITIVE RESPONSE */}
            <TabPanel>
              <Flex justify="space-between" align="center">
                <Flex align="center">
                  <Input placeholder="Search" width="300px" />
                  <Button
                    colorScheme="gray"
                    ml={2}
                    rightIcon={<ArrowDownIcon />}
                  >
                    Recent
                  </Button>
                  <Button colorScheme="gray" ml={2} rightIcon={<ArrowUpIcon />}>
                    Oldest
                  </Button>
                </Flex>
                <h1 style={{ textAlign: "right" }}>
                  Total:{" "}
                  {
                    applications.filter(
                      (application) =>
                        application.status === "Positive Response"
                    ).length
                  }
                </h1>
              </Flex>

              {applications
                  .filter((application) => application.status === "Interviewing")
                  .map((application) => (
                    <Card
                      direction={{ base: "column", sm: "row" }}
                      overflow="hidden"
                      variant="outline"
                    >
                      <Image
                        objectFit="cover"
                        maxW={{ base: "100%", sm: "200px" }}
                        src={mailPic}
                        alt="Mail"
                      />

                      <Stack>
                        <CardBody>
                          <Heading size="md">{application.company}</Heading>

                          <Text py="2">Email Body</Text>
                        </CardBody>

                        <CardFooter>
                          <Button colorScheme="gray" ml={2} onClick={() => {setMovingToInterview(true); setEditingId(application.id)}}>
                            Move To Interview Stage
                          </Button>
                          <Button colorScheme="red" ml={2} onClick={() => updateApplicationStatus(application.id, "Rejected")}>
                            Rejected
                          </Button>
                        </CardFooter>
                      </Stack>
                    </Card>
                  ))}
              


              {/* IF DONT GET WORKING IN TIME JUST USE THE BELOW CODE AS PLACEHOLDER FOR DEMO */}
              
              {/* <Card
                direction={{ base: "column", sm: "row" }}
                overflow="hidden"
                variant="outline"
              >
                <Image
                  objectFit="cover"
                  maxW={{ base: "100%", sm: "200px" }}
                  src={mailPic}
                  alt="Mail"
                />

                <Stack>
                  <CardBody>
                    <Heading size="md">Company</Heading>

                    <Text py="2">Trailing off email body...</Text>
                  </CardBody>

                  <CardFooter>
                    <Button colorScheme="gray" ml={2} onClick={() => {setMovingToInterview(true); setEditingId(application.id)}}>
                      Move To Interview Stage
                    </Button>
                    <Button colorScheme="red" ml={2} onClick={() => updateApplicationStatus(application.id, "Rejected")}>
                      Rejected
                    </Button>
                  </CardFooter>
                </Stack>
              </Card> */}
            </TabPanel>

            {/* INTERVIEWING */}
            <TabPanel>
            
              <Box display="grid" gridTemplateColumns="repeat(3, 1fr)" gap={6}>
                {applications
                  .filter((application) => application.status === "Interviewing")
                  .map((application) => (
                    <Card key={application.id} maxW="sm">
                      <CardBody>
                        <Stack mt="6" spacing="3">
                          <Heading size="md">
                            Interview with {application.company}
                          </Heading>
                          <Text>
                            {application.interview_notes}
                          </Text>
                          <Text color="blue.600" fontSize="2xl">
                            Interview Date
                          </Text>
                          <p>{application.interview_dates}</p>
                        </Stack>
                      </CardBody>
                      <Divider />
                      <CardFooter>
                        <ButtonGroup spacing="2" justifyContent="center" width="100%">
                          {/* Do same modal as move to interview stage */}
                          <Button variant="solid" colorScheme="blue">
                            Edit 
                          </Button>
                          <Button variant="ghost" colorScheme="blue" onClick={() => {setMovingToOffer(true); setEditingId(application.id)}}>
                            Move to Offer Stage
                          </Button>
                          <Button variant="ghost" colorScheme="red" onClick={() => updateApplicationStatus(application.id, "Rejected")}>
                            Rejected
                          </Button>
                        </ButtonGroup>
                      </CardFooter>
                    </Card>
                  ))}
              </Box>
           
              {/* <br></br>
              <Divider />
              <Accordion allowToggle>
                <AccordionItem>
                  <h2>
                    <AccordionButton>
                      <Box as="span" flex="1" textAlign="left">
                        <h1
                          style={{
                            textAlign: "left",
                            fontWeight: "bold",
                            color: "gray",
                          }}
                        >
                          Past Interviews
                        </h1>
                      </Box>
                      <AccordionIcon />
                    </AccordionButton>
                  </h2>
                  <AccordionPanel pb={4}></AccordionPanel>
                </AccordionItem>
              </Accordion> */}
            </TabPanel>

            {/* REJECTED */}
            <TabPanel>
              {/* Headline */}
              <Flex justify="space-between" align="center">
                <Flex align="center">
                  <Input placeholder="Search" width="300px" />
                  <Button
                    colorScheme="gray"
                    ml={2}
                    rightIcon={<ArrowDownIcon />}
                  >
                    Recent
                  </Button>
                  <Button colorScheme="gray" ml={2} rightIcon={<ArrowUpIcon />}>
                    Oldest
                  </Button>
                </Flex>
                <h1 style={{ textAlign: "right" }}>
                  Total:{" "}
                  {
                    applications.filter(
                      (application) => application.status === "Rejected"
                    ).length
                  }
                </h1>
              </Flex>
              <br></br>

              {/* List */}
              <Accordion allowToggle>
                {applications
                  .filter((application) => application.status === "Rejected")
                  .map((application) => (
                    <AccordionItem key={application.id}>
                      {" "}
                      {/* Iterating through each application (all tab) */}
                      <h2>
                        <AccordionButton
                          _expanded={{ color: "white", bg: "blue.500" }}
                        >
                          <Box as="span" flex="1" textAlign="left">
                            <Box as="span" fontWeight="bold">
                              {application.company || "Company Not Specified"}
                            </Box>
                            ,{" "}
                            <Box as="span" fontStyle="italic">
                              {application.position || "Position Not Specified"}
                            </Box>
                            <br />
                            Applied:{" "}
                            {new Date(
                              application.applied_date
                            ).toLocaleDateString()}
                            <br></br>
                            Rejected: {application.last_update}
                          </Box>
                          <Box
                            // as="span"
                            // flex="1"
                            // textAlign="right"
                            // borderRadius="full"
                            // border="2px solid"
                            // borderColor="blue.500"
                            // px={3}
                            // py={1}
                            // display="inline-block"
                            // maxW="160px"
                          >
                            {application.status}
                          </Box>
                          <AccordionIcon />
                        </AccordionButton>
                      </h2>
                      <AccordionPanel pb={4}>
                        <p>Location:</p>
                        <p style={{ textIndent: "20px" }}>
                          {application.location}
                        </p>
                        <p>Salary:</p>
                        <p style={{ textIndent: "20px" }}>
                          {application.salary}
                        </p>
                        <p>Job Description:</p>
                        <p style={{ textIndent: "20px" }}>
                          {application.job_description}
                        </p>
                        <p>Notes:</p>
                        <p style={{ textIndent: "20px" }}>
                          {application.notes}
                        </p>
                        {emails
                          .filter((email) => email.app === application.id)
                          .map((email) => (
                            <div>
                              <p>Email:</p>
                              <p style={{ textIndent: "20px" }}>
                                {email.body || "Unknown"}
                              </p>
                            </div>
                          ))}
                        <br />
                        {/* <Button colorScheme="gray">Edit</Button>{" "} */}
                        {/* Make circular */}
                        <Button
                          colorScheme="red"
                          ml={2}
                          onClick={() => handleDelete(application.id)}
                        >
                          Delete
                        </Button>
                      </AccordionPanel>
                    </AccordionItem>
                  ))}
              </Accordion>
            </TabPanel>

            {/* OFFERS */}
            <TabPanel>
              
              <Box display="grid" gridTemplateColumns="repeat(3, 1fr)" gap={6}>
                  {applications
                    .filter((application) => application.status === "Offer")
                    .map((application) => (
                      <Card key={application.id} maxW="sm">
                        <CardBody>
                          <Stack mt="6" spacing="3">
                            <Heading size="md">Offer from {application.company}</Heading>
                            <Text color="black.600" fontSize="xl">
                              San Francisco, CA
                            </Text>

                            <Text color="blue.600" fontSize="2xl">
                              Interest 
                            </Text>
                            <Text>
                              {application.offer_interest}/10
                              <br></br>
                            </Text>

                            <Text color="blue.600" fontSize="2xl">
                              Notes
                            </Text>
                            <Text>
                              {application.offer_notes}
                              <br></br>
                            </Text>
                          </Stack>
                        </CardBody>
                        <Divider />
                        <CardFooter>
                          <ButtonGroup spacing="2" justifyContent="center" width="100%">
                            <Button variant="solid" colorScheme="blue">
                              Edit
                            </Button>
                            {/* <Button variant="ghost" colorScheme="blue">Accept</Button> */}
                            <Button variant="ghost" colorScheme="blue" onClick={() => updateApplicationStatus(application.id, "Denied Offer")}>
                              Deny
                            </Button>
                          </ButtonGroup>
                        </CardFooter>
                      </Card>
                  ))}
              </Box>


              <br></br>
              <Divider />
              <Accordion allowToggle>
                <AccordionItem>
                  <h2>
                    <AccordionButton>
                      <Box as="span" flex="1" textAlign="left">
                        <h1
                          style={{
                            textAlign: "left",
                            fontWeight: "bold",
                            color: "gray",
                          }}
                        >
                          Denied Offers
                        </h1>
                      </Box>
                      <AccordionIcon />
                    </AccordionButton>
                  </h2>
                  <AccordionPanel pb={4}>
                    <Box display="grid" gridTemplateColumns="repeat(3, 1fr)" gap={6}>
                      {applications
                        .filter((application) => application.status === "Denied Offer")
                        .map((application) => (
                          <Card key={application.id} maxW="sm">
                            <CardBody>
                              <Stack mt="6" spacing="3">
                                <Heading size="md">Offer from {application.company}</Heading>
                                <Text color="black.600" fontSize="xl">
                                  San Francisco, CA
                                </Text>

                                <Text color="blue.600" fontSize="2xl">
                                  Interest 
                                </Text>
                                <Text>
                                  {application.offer_interest}/10
                                  <br></br>
                                </Text>

                                <Text color="blue.600" fontSize="2xl">
                                  Notes
                                </Text>
                                <Text>
                                  {application.offer_notes}
                                  <br></br>
                                </Text>
                              </Stack>
                            </CardBody>
                            <Divider />
                            <CardFooter>
                              <ButtonGroup spacing="2" justifyContent="center" width="100%">
                                <Button variant="solid" colorScheme="blue">
                                  Edit
                                </Button>
                                {/* <Button variant="ghost" colorScheme="blue">Accept</Button>
                                <Button variant="ghost" colorScheme="blue" onClick={() => updateApplicationStatus(application.id, "Denied Offer")}>
                                  Deny
                                </Button> */}
                              </ButtonGroup>
                            </CardFooter>
                          </Card>
                      ))}
                    </Box>
                  </AccordionPanel>
                </AccordionItem>
              </Accordion>
            </TabPanel>
          </TabPanels>
        </Tabs>

        {/* Move To Interview Modal */}
        <Modal isOpen={movingToInterview} onClose={() => {setMovingToInterview(false); setEditingId(null);}} size="xl">
          <ModalContent>
            <ModalHeader>Add Interview Details</ModalHeader>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleMoveToInterview(editingId, moveToInterviewForm); 
                setMovingToInterview(false);
              }}
            >
              <ModalBody>
                <Grid templateColumns="repeat(2, 1fr)" gap={4}>
                  
                  <GridItem>
                    <FormControl id="interview_notes" isRequired>
                      <FormLabel>Notes</FormLabel>
                      <Input
                        type="text"
                        name="interview_notes"
                        value={moveToInterviewForm.interview_notes}
                        onChange={(e) =>
                          setMoveToInterviewForm((prev) => ({
                            ...prev,
                            interview_notes: e.target.value,
                          }))
                        }
                        placeholder="i.e. 45 minute Technical Interview. Dress code: Business Casual"
                      />
                    </FormControl>
                  </GridItem>

                  <GridItem>
                    <FormControl id="interview_dates" isRequired>
                      <FormLabel>Interview Date</FormLabel>
                      <Input
                        type="text"
                        name="interview_dates"
                        value={moveToInterviewForm.interview_dates}
                        onChange={(e) =>
                          setMoveToInterviewForm((prev) => ({
                            ...prev,
                            interview_dates: e.target.value,
                          }))
                        }
                        placeholder="YYYY-MM-DD"
                      />
                    </FormControl>
                  </GridItem>
                </Grid>
              </ModalBody>

              <ModalFooter>
                <Button colorScheme="red" mr={3} onClick={() => setMovingToInterview(false)}>Cancel</Button>
                <Button colorScheme="gray" type="submit" rightIcon={<ArrowForwardIcon />}>Move</Button>
              </ModalFooter>
            </form>
          </ModalContent>
        </Modal>


        {/* Move To Offer Modal */}
        <Modal isOpen={movingToOffer} onClose={() => setMovingToOffer(false)} size="xl">
          <ModalContent>
            <ModalHeader>Add Offer Details</ModalHeader>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleMoveToOffer(editingId, moveToOfferForm); 
                setMovingToOffer(false);
              }}
            >
              <ModalBody>
                <Grid templateColumns="repeat(2, 1fr)" gap={4}>
                  
                  <GridItem>
                    <FormControl id="offer_notes" isRequired>
                      <FormLabel>Notes</FormLabel>
                      <Input
                        type="text"
                        name="offer_notes"
                        value={moveToOfferForm.offer_notes}
                        onChange={(e) =>
                          setMoveToOfferForm((prev) => ({
                            ...prev,
                            offer_notes: e.target.value,
                          }))
                        }
                        placeholder="i.e. Any notes about the offer!"
                      />
                    </FormControl>
                  </GridItem>

                  <GridItem>
                    <FormControl id="offer_interest" isRequired>
                      <FormLabel>Offer Interest</FormLabel>
                      <Input
                        type="text"
                        name="offer_interest"
                        value={moveToOfferForm.offer_interest}
                        onChange={(e) =>
                          setMoveToOfferForm((prev) => ({
                            ...prev,
                            offer_interest: e.target.value,
                          }))
                        }
                        placeholder="Value 1-10"
                      />
                    </FormControl>
                  </GridItem>
                </Grid>
              </ModalBody>

              <ModalFooter>
                <Button colorScheme="red" mr={3} onClick={() => setMovingToOffer(false)}>Cancel</Button>
                <Button colorScheme="gray" type="submit" rightIcon={<ArrowForwardIcon />}>Move</Button>
              </ModalFooter>
            </form>
          </ModalContent>
        </Modal>

      </ChakraProvider>
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default Applications;
