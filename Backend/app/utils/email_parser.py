import spacy
import re

# Load spaCy's pre-trained English model
nlp = spacy.load("en_core_web_sm")

# List of common job titles (this can be expanded as needed)
job_titles = [
    "Software Engineer", "Software Developer", "Data Scientist", "Data Engineer",
    "Project Manager", "Web Developer", "UX Designer", "DevOps Engineer", "Backend Developer",
    "Frontend Developer", "Product Manager", "AI Engineer", "Research Scientist", "QA Engineer"
]

# Function to extract company names and job positions
def extract_company_and_position(email_body):
    doc = nlp(email_body)
    entities = {
        "company": None,
        "position": None
    }
    
    print(doc.ents)
    
    # Extract company name (first ORG entity)
    for ent in doc.ents:
        if ent.label_ == "ORG" and not entities["company"]:
            entities["company"] = ent.text  # First organization found is considered the company

    # Extract job title by looking for keywords in the text
    for sentence in doc.sents:  # Check each sentence in the email body
        for job in job_titles:
            if job.lower() in sentence.text.lower():
                entities["position"] = job
                break  # Stop after finding the first job title

    return entities

possible_companies = [
    "Google", "Microsoft", "Apple", "Amazon", "Facebook", "Twitter", "LinkedIn", "Netflix", "Spotify",
    "Uber", "Lyft", "Airbnb", "Slack", "Dropbox", "Salesforce", "Oracle", "IBM", "Intel", "Nvidia",
    "Qualcomm", "Cisco", "HP", "Dell", "Samsung", "Sony", "Panasonic", "LG", "Toshiba", "Nokia",
    "Motorola", "Xerox", "Adobe", "VMware", "PayPal", "Square", "Stripe", "Reddit", "Pinterest",
    "Snapchat", "TikTok", "Zoom", "Epic Games", "Unity", "Riot Games", "Activision", "Blizzard",
    "Sony", "Nintendo", "Sega", "Capcom", "Bandai Namco", "Konami", "Square Enix", "Ubisoft", "Lucid", "Playstation", "SingleStore"
]

status_updates = [
    "received", "declined", "rejected", "accepted", "interview", "offer", "position", "application", "resume", "job", "opportunity",
    "candidate", "recruiter", "hiring", "manager", "team", "role", "experience", "skills", "qualification", "schedule", "availability", "not been selected"
]

job_positions = [ "Software Engineer", "Data Scientist", "Product Manager", "UX Designer", "Project Manager", "QA Engineer", "DevOps Engineer", "Web Developer", "Software Engineering Intern", "Data Science Intern", "Product Management Intern", "UX Design Intern", "Project Management Intern", "QA Intern", "DevOps Intern", "Web Development Intern" ]

rejection_keywords = [ "not been selected", "not selected", "application unsuccessful", "declined", "rejected" ]


def parse_email_data_hardcoded(email_body):
    company = None
    position = None
    status = "Unknown"  # Default status

    # Lowercase the email body for case-insensitive matching
    email_body_lower = email_body.lower()

    # Find the company (stop at first match)
    for c in possible_companies:
        # Use regex to match the company name, allowing for trailing punctuation like !,.?
        if re.search(rf"\b{re.escape(c.lower())}[\s\.\,\!\?]*", email_body_lower):
            company = c
            break  # Stop after finding the first matching company


    # Search for status updates in the email body
    for update in status_updates:
        # Use regex to match the status, allowing for trailing punctuation
        if re.search(rf"\b{re.escape(update.lower())}[\s\.\,\!\?]*", email_body_lower):
            # If a rejection phrase is found, set status to "Rejected"
            if any(re.search(rf"\b{re.escape(rj.lower())}[\s\.\,\!\?]*", email_body_lower) for rj in rejection_keywords):
                status = "Rejected"
            else:
                status = update.capitalize()  # Default to the status found (e.g., "Rejected")
            break  # Stop after finding the first matching status
        
    # Find the job position (stop at first match)
    for pos in job_positions:
        if re.search(rf"\b{re.escape(pos.lower())}[\s\.\,\!\?]*", email_body_lower):
            position = pos
            # if next word is "intern" or "Intern", add it to the position
            if re.search(rf"\bintern\b", email_body_lower):
                position += " Intern"
            break  # Stop after finding the first matching position
        else:
            position = "Unknown"

    return {"company": company, "position": position, "status": status}