import React, { useState, useEffect } from "react";

//Chakra
import { ChakraProvider, HStack } from "@chakra-ui/react";
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

  /* Create Application Dialogue Box */
  const [creatingApplication, setCreatingApplication] = useState(false);
  const handleCreate = async () => {
    try {
      const response = await fetch(
        "http://localhost:8000/application/create_application",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${authTokens}`,
          },
          body: JSON.stringify(formData),
        }
      );

      if (response.ok) {
        fetchApplications();
        setFormData({
          company: "",
          position: "",
          location: "",
          status: "",
          applied_date: "",
          last_update: "",
          salary: "",
          job_description: "",
          notes: "",
        });
      } else {
        throw new Error("Failed to create application");
      }
    } catch (err) {
      setError(err.message);
    }
  };
  const [formData, setFormData] = useState({
    company: "",
    position: "",
    status: "",
    applied_date: "",
    notes: "",
  });

  /* Applications List */
  const [applications, setApplications] = useState([]);
  const [editingId, setEditingId] = useState(null);
  useEffect(() => {
    fetchApplications();
    fetchTheme();
  }, []);

  //Handlers
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
        setApplications(data);
      } else {
        throw new Error("Failed to fetch applications");
      }
    } catch (err) {
      setError("Error fetching applications");
    }
  };
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

  //Themes
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
        <Modal
          isOpen={creatingApplication}
          onClose={() => setCreatingApplication(false)}
          size="xl"
        >
          <ModalContent>
            <ModalHeader>New Application</ModalHeader>
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleCreate();
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
                        value={formData.company}
                        onChange={(e) =>
                          setFormData((prev) => ({
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
                        value={formData.position}
                        onChange={(e) =>
                          setFormData((prev) => ({
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
                        value={formData.location}
                        onChange={(e) =>
                          setFormData((prev) => ({
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
                        value={formData.salary}
                        onChange={(e) =>
                          setFormData((prev) => ({
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
                          setFormData((prev) => ({ ...prev, status: value }))
                        }
                        value={formData.status}
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
                        value={formData.job_description}
                        onChange={(e) =>
                          setFormData((prev) => ({
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
                        value={formData.notes}
                        onChange={(e) =>
                          setFormData((prev) => ({
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
              <Tooltip label="Update applications from email">
                <IconButton colorScheme="gray" icon={<RepeatIcon />} mr={2} />
              </Tooltip>

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
                            {application.company}
                          </Box>
                          ,{" "}
                          <Box as="span" fontStyle="italic">
                            {application.position}
                          </Box>
                          <br />
                          Applied: 11/4/24
                        </Box>
                        <Box
                          as="span"
                          flex="1"
                          textAlign="right"
                          borderRadius="full"
                          border="2px solid"
                          borderColor="blue.500"
                          px={3}
                          py={1}
                          display="inline-block"
                          maxW="160px"
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
                      <br />
                      <Button colorScheme="gray">Edit</Button>{" "}
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
                
            {/* AWAITING RESPONSE */}
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
                  Total: {applications.filter((application) => application.status === "Awaiting Response").length}
                </h1>
              </Flex>
              <br></br>

              {/* List */}
              <Accordion allowToggle>
                {applications.filter((application) => application.status === "Awaiting Response").map((application) => (
                  <AccordionItem key={application.id}>
                    {" "}
                    {/* Iterating through each application (all tab) */}
                    <h2>
                      <AccordionButton
                        _expanded={{ color: "white", bg: "blue.500" }}
                      >
                        <Box as="span" flex="1" textAlign="left">
                          <Box as="span" fontWeight="bold">
                            {application.company}
                          </Box>
                          ,{" "}
                          <Box as="span" fontStyle="italic">
                            {application.position}
                          </Box>
                          <br />
                          Applied: 11/4/24
                        </Box>
                        <Box
                          as="span"
                          flex="1"
                          textAlign="right"
                          borderRadius="full"
                          border="2px solid"
                          borderColor="blue.500"
                          px={3}
                          py={1}
                          display="inline-block"
                          maxW="160px"
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
                      <br />
                      <Button colorScheme="gray">Edit</Button>{" "}
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

            {/* POSITIVE RESPONSE */}
            <TabPanel>
              
            </TabPanel>

            {/* INTERVIEWING */}
            <TabPanel>
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
                  Total: {applications.filter((application) => application.status === "Rejected").length}
                </h1>
              </Flex>
              <br></br>

              {/* List */}
              <Accordion allowToggle>
                {applications.filter((application) => application.status === "Rejected").map((application) => (
                  <AccordionItem key={application.id}>
                    {" "}
                    {/* Iterating through each application (all tab) */}
                    <h2>
                      <AccordionButton
                        _expanded={{ color: "white", bg: "blue.500" }}
                      >
                        <Box as="span" flex="1" textAlign="left">
                          <Box as="span" fontWeight="bold">
                            {application.company}
                          </Box>
                          ,{" "}
                          <Box as="span" fontStyle="italic">
                            {application.position}
                          </Box>
                          <br />
                          Applied: 11/4/24
                          <br></br>
                          Rejected: 11/5/24
                          
                        </Box>
                        <Box
                          as="span"
                          flex="1"
                          textAlign="right"
                          borderRadius="full"
                          border="2px solid"
                          borderColor="blue.500"
                          px={3}
                          py={1}
                          display="inline-block"
                          maxW="160px"
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
                      <br />
                      <Button colorScheme="gray">Edit</Button>{" "}
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
              
            </TabPanel>

          </TabPanels>
        </Tabs>
      </ChakraProvider>
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default Applications;