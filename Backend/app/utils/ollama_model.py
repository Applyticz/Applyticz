import ollama

# Pull the model first
ollama.pull('llama3.1')

prompt = "parse the email body to return the company name, job position, and status (only return this information). The email body is as follows:"

# Define the email messages to process
email_messages = [
    {
        'role': 'user',
        'content': f'{prompt} "Hi Alec-Nesat, Thank you for applying for our Software Engineer Internship 2025 role here at Lucid Software. We have received a great number of applications from many qualified applicants. Although we appreciate your interest in Lucid, at this time you have not been selected to move forward in the hiring process. We have selected candidates whose experience and qualifications are more aligned with our needs at this time. We appreciate the effort you put into applying, and we encourage you to check our job postings regularly. Should there be a position that is of interest to you, we hope you reapply. We wish you the best in your future employment search. Best regards, The Lucid Software Recruiting Team."',
    },
    {
        'role': 'user',
        'content': f'{prompt} "Hi Alec-Nesat, Thank you for applying to PlayStation Global for the Software Engineering Intern - Undergraduate opportunity. Your application has been received and will be reviewed. Please be on the lookout for future correspondence. Regards, PlayStation Talent Acquisition ** Please note: Do not reply to this email. This email is sent from an unattended mailbox. Replies will not be read."',
    }
]

# Process each email message
for message in email_messages:
    try:
        response = ollama.chat(model='llama3.1', messages=[message])
        print(response['message']['content'])
    except Exception as e:
        print(f"An error occurred: {e}")