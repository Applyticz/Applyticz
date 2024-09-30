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

                    <TabPanel>
                        <p>1st Tab Content</p>
                    </TabPanel>

                    <TabPanel>
                        <p>Order Most Recent First</p>
                    </TabPanel>

                    <TabPanel>
                        <p>Depending on the positive response you can manually decide to move to interview stage</p>
                    </TabPanel>

                    <TabPanel>
                        <p>In this tab we can have some sort of Interview tracker to track all stages within</p>
                        {/* <p>Basically an entirely seperate tracker within... i think itd make it easier and be more detailed</p> */}
                        {/* that way you can use the overarching tabs as a main overview but wunna dial in on interview stuff so seperate thing */}
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