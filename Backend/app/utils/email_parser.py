import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")

def extract_email_fields(email_body):
    # Process the email body text with SpaCy
    doc = nlp(email_body)
    
    parsed_application = {
        "company": "Unknown",
        "position": "Unknown",
        "location": "Unknown",
        "status": "Unknown",
        "salary": "Unknown",
        "job_description": "Not provided",
        "notes": ""
    }
    
        # Extract entities using NER
    for ent in doc.ents:
        if ent.label_ == "ORG":
            # Organization names often refer to the company
            parsed_application["company"] = ent.text
        elif ent.label_ == "GPE":
            # Geographic location for job location
            parsed_application["location"] = ent.text
        elif ent.label_ == "MONEY":
            # Salary information
            parsed_application["salary"] = ent.text
        elif ent.label_ == "PERSON":
            # Position could be associated with a person, but it needs more context
            parsed_application["position"] = ent.text

    # Use keyword matching or pattern matching to extract other information
    if "application received" in email_body.lower():
        parsed_application["status"] = "Application Received"
    elif "interview scheduled" in email_body.lower():
        parsed_application["status"] = "Interview Scheduled"
    elif "rejected" in email_body.lower():
        parsed_application["status"] = "Rejected"
    elif "offer" in email_body.lower():
        parsed_application["status"] = "Offer Extended"
    
    # Look for common job-related terms to identify job descriptions and positions
    if "job description" in email_body.lower():
        parsed_application["job_description"] = email_body.split("Job Description:")[-1].strip()

    # Extract any remaining notes from the body as additional context
    parsed_application["notes"] = email_body.strip()

    return parsed_application

    