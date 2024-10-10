import React, { useState, useEffect } from 'react';
import useAuth from "../../utils";
import "../../App.css";

//Chakra
import { ChakraProvider } from '@chakra-ui/react'
import {Modal, ModalContent, ModalHeader, ModalFooter, ModalBody} from '@chakra-ui/react'
import { Button, ButtonGroup } from '@chakra-ui/react'
import { Input } from '@chakra-ui/react'


//GMAIL API STUFF:
    //We have our client secret IDs and stuff, and applyticz is registered
    //May need to change callback and figure out what that does-> how that works to get the tokens
    //Then the consent screen -> need to add a new email for test users

//We have the option for users to add their Gmail Account or not -> kinda like a beta or something atm

//REFRESH TOKEN URL:
//https://oauth2.googleapis.com/token



function LinkedAccounts(){
    const { authTokens } = useAuth();
    const [applications, setApplications] = useState([]);
    const [error, setError] = useState('');


    
    //Gmail Adding & Authentication
    const [addingNewGmail, setAddingNewGmail] = useState(false);  //Modal
    // const [gmailInput, setGmailInput] = useState('');             //Modal Gmail Input
    // const handleGmailInputChange = (event) => {
    //     setGmailInput(event.target.value);
    // }
    // const authenticateGmail = async() => {
    //     //Send the email to the backend (or just to Gmail API)
    //     //console.log(gmailInput);
    // }
    
    const gmailAuthServer = "https://accounts.google.com/o/oauth2/v2/auth?"
    const clientID = "client_id=540720712071-3ki8o3kpog4int741skr5rb817lo2543.apps.googleusercontent.com"
    const redirectURI = "&redirect_uri=https%3A%2F%2Flocalhost%3A8000%2Fgmail_api%2Fcallback"
    const responseType = "&response_type=code"
    const scopes = "&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.readonly"
    const redirectToOAuthConsentScreen = async() =>{
        const gmailAuthenticationLink = gmailAuthServer + clientID + redirectURI + responseType + scopes;
        window.location.href = gmailAuthenticationLink;
    }



    
    return(
        <>
            <h2>Linked Accounts (fix styling)</h2>
            <ChakraProvider>
                <h1>Gmail</h1>
                    <p>List Current Linked Accounts HERE</p>
                    <Button colorScheme='gray' onClick={() => setAddingNewGmail(true)}>Link New Account</Button>


                <br></br>
                <br></br>
                <br></br>
                <h1>Outlook</h1>


                {/* MODALS -> Do as a stepper form instead */}
                <Modal isOpen={addingNewGmail} onClose={() => addingNewGmail(false)}>
                    <ModalContent>
                        <ModalHeader>Add Gmail Account</ModalHeader>
                
                        <ModalBody>
                            <p>
                                To link your Gmail account and enable automatic updates, Google authentication is required. By clicking
                                the "Authenticate" button below, you will be redirected to their authentication and consent screen where you can 
                                grant Applyticz read only access to your email. This is entirely optional, and Applyticz can still be used manually if you choose not
                                to grant email permissions, however, you will not be able to use the automatic update features.
                            </p>
                            {/* <Input placeholder='example@gmail.com' size='xs' onChange={handleGmailInputChange}/> */}
                        </ModalBody>

                        <ModalFooter>
                            <Button colorScheme='red' mr={3} onClick={() => setAddingNewGmail(false)}>Cancel</Button>
                            <Button colorScheme='gray' onClick={redirectToOAuthConsentScreen}>Authenticate</Button>
                        </ModalFooter>
                    </ModalContent>
                </Modal>
            </ChakraProvider>
            
        </>
    );
}

export default LinkedAccounts;