import React, { useState, useEffect } from 'react';
import useAuth from "../../utils";


function LinkedEmails(){
    const { authTokens } = useAuth();
    const [applications, setApplications] = useState([]);
    const [error, setError] = useState('');
    
    return(
        <>
        <p>Test</p>
        </>
    );
}

export default LinkedEmails;