// import React, { useState, useEffect } from 'react';
// import { ChakraProvider } from '@chakra-ui/react'
// import { Tabs, TabList, TabPanels, Tab, TabPanel } from '@chakra-ui/react'
// import {Accordion, AccordionItem, AccordionButton, AccordionPanel, AccordionIcon, Box, Button} from '@chakra-ui/react'

// import "./ApplicationsPage.css";
// import "../../App.css";
// import useAuth from "../../utils";



// function Tabbing() {
//   const { authTokens } = useAuth();
//   const [applications, setApplications] = useState([]); 
//   const [editingId, setEditingId] = useState(null);
//   useEffect(() => {
//     fetchApplications();
//     fetchTheme();
//   }, []); 


//   //Handlers
//   const fetchApplications = async () => {
//     try {
//       const response = await fetch("http://localhost:8000/application/get_applications", {
//         headers: {
//           "Authorization": `Bearer ${authTokens}`
//         }
//       });
//       if (response.ok) {
//         const data = await response.json();
//         setApplications(data);
//       } else {
//         throw new Error('Failed to fetch applications');
//       }
//     } catch (err) {
//       setError('Error fetching applications');
//     }
//   };
//   const handleInputChange = (e, applicationId) => {
//     const { name, value } = e.target;
//     setApplications(prevApplications => prevApplications.map(app => 
//       app.id === applicationId ? { ...app, [name]: value } : app
//     ));
//   };
//   const handleSubmit = async (applicationId) => {

//     try {
//       const updatedApplication = applications.find(app => app.id === applicationId);
//       const response = await fetch(`http://localhost:8000/application/update_application`, {
//         method: 'PUT',
//         headers: {
//           "Content-Type": "application/json",
//           "Authorization": `Bearer ${authTokens}`
//         },
//         body: JSON.stringify(updatedApplication)
//       });

//       if (response.ok) {
//         setEditingId(null);
//         fetchApplications();
//       } else {
//         throw new Error('Failed to update application');
//       }
//     } catch (err) {
//       setError(err.message);
//     }
//   };
//   const handleDelete = async (id) => {
//     try {
//       const response = await fetch(`http://localhost:8000/application/delete_application?id=${id}`, {
//         method: 'DELETE',
//         headers: {
//           "Authorization": `Bearer ${authTokens}`
//         }
//       });

//       if (response.ok) {
//         fetchApplications();
//       } else {
//         throw new Error('Failed to delete application');
//       }
//     } catch (err) {
//       setError('Error deleting application');
//     }
//   };


//   //Themes
//   const [theme, setTheme] = useState('light');
//   const fetchTheme = async () => {
//     try {
//       const response = await fetch("http://localhost:8000/settings/get_settings", {
//         headers: {
//           "Authorization": `Bearer ${authTokens}`
//         }
//       });
//       if (response.ok) {
//         const data = await response.json();
//         setTheme(data.theme || 'light');
//       } else {
//         throw new Error('Failed to fetch theme');
//       }
//     } catch (err) {
//       setError('Error fetching theme');
//     }
//   };
//   useEffect(() => {
//     // Apply the theme by toggling class on the root element
//     const root = document.documentElement;
//     root.classList.remove('light', 'dark');
//     root.classList.add(theme);
//   }, [theme]);


//   return (
//     <div>
//         <ChakraProvider>
//             <Tabs variant='soft-rounded'>
//                 <TabList>
//                     {/* Have number at top of each tab! */}
//                     <Tab _selected={{ color: 'white', bg: 'blue.500' }}>All</Tab>
//                     <Tab _selected={{ color: 'white', bg: 'yellow.400' }}>Awaiting Response</Tab>
//                     <Tab _selected={{ color: 'white', bg: 'green.400' }}>Positive Response</Tab>

//                     {/* Maybe in this tab you have an interview Tracker Inside, so can keep track of everything w interviews all in one place */}
//                     <Tab _selected={{ color: 'white', bg: 'teal.300' }}>Interviewing</Tab>  
//                     <Tab _selected={{ color: 'white', bg: 'red.400' }}>Rejected</Tab>
//                     <Tab _selected={{ color: 'white', bg: 'purple.300' }}>Offers</Tab>  
//                 </TabList>


//                 <TabPanels>

//                     {/* For each tab it should show different information? */}
//                     {/* <p>IDEAS/STRUCTURE FOR EACH TAB:</p>
//                        <br></br>
//                         <p>ALL, AWIAITING RESPONSE, REJECTED</p>
//                             <p>it should be more like a table format with thin boxes one on top of other (Table format like - Since we have so many)
//                             </p>
//                             <p>Needs search functionality and default sort to newest first, but be able to change (by clicking up or down arrow - down currently selected)</p>
//                             <br></br>
//                         <p> INTERVIEWING</p>
//                         <p>Box format with tri column staging visual (with right and left arrows on each BOX to move between stages) - since not many at a time</p>
                        
//                         <br>
//                         </br>
//                         <p>OFFERS</p>
//                         <p>Have it be more like a comparison of salary, benefits, location, interest (shown in stars) 1-10 stars and order by priority</p>

//                         <br></br>
//                         <p>POSITIVE RESPONSES</p>
//                         <p>These will be pulled from email and indicate a response that needs to done and maybe like staging area where you can go from like NeedsAction and move to SentMyResponse 
//                             Or buttons that move it to rejected/interviewing tab depending
//                         </p> */}



//                     <TabPanel>
//                         <h1 style={{textAlign: 'right'}}>Total: {applications.length} </h1>
//                         <br></br>
//                         <Accordion allowToggle>
//                             {applications.map((application) => (
//                                 <AccordionItem key={application.id}>  {/* Iterating through each application (all tab) */}
//                                     <h2>
//                                         <AccordionButton _expanded={{color: 'white', bg: 'blue.500'}}>
//                                             <Box as="span" flex="1" textAlign="left" >
//                                                 <Box as="span" fontWeight="bold">{application.company}</Box>
//                                                 ,{" "}
//                                                 <Box as="span" fontStyle="italic">{application.position}</Box>
//                                                 <br />
//                                                 11/4/24
//                                             </Box>
//                                             <Box 
//                                                 as="span" 
//                                                 flex="1" 
//                                                 textAlign="right" 
//                                                 borderRadius="full" 
//                                                 border="2px solid" 
//                                                 borderColor="blue.500" 
//                                                 px={3} 
//                                                 py={1}
//                                                 display="inline-block"
//                                                 maxW="160px"
//                                                 >
//                                                 {application.status}
//                                                 </Box>
//                                         <AccordionIcon />
//                                         </AccordionButton>
//                                     </h2>
//                                     <AccordionPanel pb={4}>
//                                         <p>Stage: {application.status}</p>
//                                         <p>Applied Date: {application.applied_date}</p>
//                                         <p>Last Update: {application.last_update}</p>
//                                         <p>Notes: {application.notes}</p>
//                                         <Button colorScheme='gray'>Edit</Button> {/* Make circular */}
//                                     </AccordionPanel>
//                                 </AccordionItem>
//                             ))}
//                         </Accordion> 
                    







//                         {/* <div className="applications-list">
//                             {applications.map((application) => (
//                             <div key={application.id} className="application-item">
//                                 <h3>{application.company} - {application.position}</h3>
//                                 {editingId === application.id ? (
//                                 <div className="application-edit-form">
//                                     <input
//                                     type="text"
//                                     name="company"
//                                     value={application.company}
//                                     onChange={(e) => handleInputChange(e, application.id)}
//                                     placeholder="Company"
//                                     required
//                                     />
//                                     <input
//                                     type="text"
//                                     name="position"
//                                     value={application.position}
//                                     onChange={(e) => handleInputChange(e, application.id)}
//                                     placeholder="Position"
//                                     required
//                                     />
//                                     <input
//                                     type="text"
//                                     name="location"
//                                     value={application.location}
//                                     onChange={(e) => handleInputChange(e, application.id)}
//                                     placeholder="Location"
//                                     required
//                                     />
//                                     <input
//                                     type="text"
//                                     name="status"
//                                     value={application.status}
//                                     onChange={(e) => handleInputChange(e, application.id)}
//                                     placeholder="Status"
//                                     required
//                                     />
//                                     <input
//                                     type="text"
//                                     name="salary"
//                                     value={application.salary}
//                                     onChange={(e) => handleInputChange(e, application.id)}
//                                     placeholder="Salary"
//                                     required
//                                     />
//                                     <textarea
//                                     name="job_description"
//                                     value={application.job_description}
//                                     onChange={(e) => handleInputChange(e, application.id)}
//                                     placeholder="Job Description"
//                                     />
//                                     <textarea
//                                     name="notes"
//                                     value={application.notes}
//                                     onChange={(e) => handleInputChange(e, application.id)}
//                                     placeholder="Notes"
//                                     />
//                                     <div className="button-group">
//                                     <button onClick={() => handleSubmit(application.id)} className="save">Save</button>
//                                     <button onClick={() => setEditingId(null)} className="cancel">Cancel</button>
//                                     </div>
//                                 </div>
//                                 ) : (
//                                 <div className="application-display">
//                                     <p>Stage: {application.status}</p>
//                                     <p>Applied Date: {application.applied_date}</p>
//                                     <p>Last Update: {application.last_update}</p>
//                                     <p>Notes: {application.notes}</p>
//                                     <div className="button-group">
//                                     <button onClick={() => setEditingId(application.id)} className="edit">Edit</button>
//                                     <button onClick={() => handleDelete(application.id)} className="delete">Delete</button>
//                                     </div>
//                                 </div>
//                                 )}
//                             </div>
//                             ))}
//                         </div>                       */}
//                     </TabPanel>



//                     <TabPanel>
                        
//                     </TabPanel>

//                     <TabPanel>
//                         <p>Depending on the positive response you can manually decide to move to interview stage via a button</p>
//                     </TabPanel>

//                     <TabPanel>
//                         <p>In this tab we can have some sort of Interview tracker to track all stages within. Maybe like 2-4 columns</p>
//                         {/* <p>Basically an entirely seperate tracker within... i think itd make it easier and be more detailed</p> */}
//                         {/* that way you can use the overarching tabs as a main overview but wunna dial in on interview stuff so seperate thing */}
//                         {/* Have them be displayed as boxes with arrows where you can move between 3 trifold columns (1st round, 2nd round, 3rd round -> and notes for each round) */}
//                     </TabPanel>

//                     <TabPanel>
//                         <p>5th Tab Content</p>
//                     </TabPanel>
//                 </TabPanels>
//             </Tabs>
//         </ChakraProvider>
           

      
//     </div>
    
//   );
// }

// export default Tabbing;