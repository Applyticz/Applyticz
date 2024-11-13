import ollama

# Pull the model first
ollama.pull('llama3.1')

# Define a parsing function that accepts the email body as an argument
def parse_email(email_body):
    prompt = (
        "parse the email body to return the company name, job position, "
        "and status (only return this information). The email body is as follows:"
    )
    
    message = {
        'role': 'user',
        'content': f'{prompt} "{email_body}"',
    }
    
    try:
        response = ollama.chat(model='llama3.1', messages=[message])
        # Assuming response['message']['content'] contains the parsed information
        parsed_data = response['message']['content']
        return parsed_data  # return the parsed response text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None  # Return None if there’s an error

# Test the parse_email function with a dummy email body
dummy_email_body = """
Hi Alec-Nesat, 

Thank you for your interest in a Software Engineering role at Twilio! We just received your application. 
We know that job hunting can be stressful. Our intention is to be transparent about our hiring process to help you succeed. 

On that note, let's talk a bit about our hiring process. 
If we like what we see, a recruiting team member will reach out to discuss the opportunity. 
The next steps could include a few rounds of interviews taking from 2-4 weeks, sometimes longer.

Thank you,
-Twilio Recruiting Team
"""

# Call the parse_email function and print the result
#parsed_data = parse_email(dummy_email_body)
#print("Parsed Data:", parsed_data)
