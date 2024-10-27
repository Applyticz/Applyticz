import React, { useState, useEffect } from 'react';

import { ChakraProvider } from '@chakra-ui/react'
import { Tabs, TabList, TabPanels, Tab, TabPanel } from '@chakra-ui/react'

function Tabbing() {
//   const { authTokens } = useAuth();
//   const [applications, setApplications] = useState([]);
//   const [error, setError] = useState('');
//   const [isCreating, setIsCreating] = useState(false);
//   const [editingId, setEditingId] = useState(null);

 

  return (
    <div>
        <ChakraProvider>
            <Tabs variant='soft-rounded'>
                <TabList>

                    {/* Have number at top of each tab! */}
                    <Tab _selected={{ color: 'white', bg: 'blue.500' }}>All</Tab>
                    <Tab _selected={{ color: 'white', bg: 'yellow.400' }}>Awaiting Response</Tab>
                    <Tab _selected={{ color: 'white', bg: 'green.400' }}>Positive Response</Tab>

                    {/* Maybe in this tab you have an interview Tracker Inside, so can keep track of everything w interviews all in one place */}
                    <Tab _selected={{ color: 'white', bg: 'teal.300' }}>Interviewing</Tab>  
                    <Tab _selected={{ color: 'white', bg: 'red.400' }}>Rejected</Tab>
                    <Tab _selected={{ color: 'white', bg: 'purple.300' }}>Offers</Tab>  
                    

                </TabList>

                <TabPanels>

                    {/* For each tab it should show different information? */}
                    {/* <p>IDEAS/STRUCTURE FOR EACH TAB:</p>
                       <br></br>
                        <p>ALL, AWIAITING RESPONSE, REJECTED</p>
                            <p>it should be more like a table format with thin boxes one on top of other (Table format like - Since we have so many)
                            </p>
                            <p>Needs search functionality and default sort to newest first, but be able to change (by clicking up or down arrow - down currently selected)</p>
                            <br></br>
                        <p> INTERVIEWING</p>
                        <p>Box format with tri column staging visual (with right and left arrows on each BOX to move between stages) - since not many at a time</p>
                        
                        <br>
                        </br>
                        <p>OFFERS</p>
                        <p>Have it be more like a comparison of salary, benefits, location, interest (shown in stars) 1-10 stars and order by priority</p>

                        <br></br>
                        <p>POSITIVE RESPONSES</p>
                        <p>These will be pulled from email and indicate a response that needs to done and maybe like staging area where you can go from like NeedsAction and move to SentMyResponse 
                            Or buttons that move it to rejected/interviewing tab depending
                        </p> */}

                    <TabPanel>
                        
                        

                    </TabPanel>

                    <TabPanel>
                        <p>Order Most Recent First</p>
                    </TabPanel>

                    <TabPanel>
                        <p>Depending on the positive response you can manually decide to move to interview stage via a button</p>
                    </TabPanel>

                    <TabPanel>
                        <p>In this tab we can have some sort of Interview tracker to track all stages within. Maybe like 2-4 columns</p>
                        {/* <p>Basically an entirely seperate tracker within... i think itd make it easier and be more detailed</p> */}
                        {/* that way you can use the overarching tabs as a main overview but wunna dial in on interview stuff so seperate thing */}
                        {/* Have them be displayed as boxes with arrows where you can move between 3 trifold columns (1st round, 2nd round, 3rd round -> and notes for each round) */}
                    </TabPanel>

                    <TabPanel>
                        <p>5th Tab Content</p>
                    </TabPanel>
                </TabPanels>
            </Tabs>
        </ChakraProvider>
           

      
    </div>
    
  );
}

export default Tabbing;