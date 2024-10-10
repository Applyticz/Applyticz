import React, { useState, useEffect } from 'react';
import useAuth from "../../utils";

//Chakra
import { ChakraProvider } from '@chakra-ui/react'
import {
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
} from '@chakra-ui/react'
import { Button, ButtonGroup } from '@chakra-ui/react'


function LinkedAccounts(){
    const { authTokens } = useAuth();
    const [applications, setApplications] = useState([]);
    const [error, setError] = useState('');
    
    return(
        <>
            <h2>Linked Accounts (fix styling)</h2>
            <ChakraProvider>
                <h1>Gmail</h1>
                    <p>List Current Linked Accounts HERE</p>
                    <Button colorScheme='gray'>Link New Account</Button>


                <br></br>
                <br></br>
                <br></br>
                <h1>Outlook</h1>
            </ChakraProvider>
            
        </>
    );
}

export default LinkedAccounts;