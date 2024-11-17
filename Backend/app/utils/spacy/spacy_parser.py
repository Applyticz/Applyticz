import re
import spacy
import os

# Resolve the absolute path to the trained model
base_dir = os.path.dirname(__file__)  # Directory of spacy_parser.py
output_dir = os.path.abspath(os.path.join(base_dir, "trained_model"))

# Print the resolved path for debugging (optional)
print(f"Loading model from: {output_dir}")

# Load the trained spaCy model
try:
    nlp = spacy.load(output_dir)
    print("Model loaded successfully.")
except Exception as e:
    raise OSError(f"Error loading model from {output_dir}: {e}")

# Status updates and rejection keywords
status_updates = [
    "received", "declined", "rejected", "accepted", "interview", "offer", "candidate", 
    "not been selected", "not selected", "application unsuccessful", "shortlisted", 
    "reviewed", "pending", "in progress", "on hold", "withdrawn", "hired", 
    "onboarding", "completed", "closed", "archived"
]
rejection_keywords = [
    "not been selected", "not selected", "application unsuccessful", "declined", "rejected"
]

# Updated email parser function
def parse_email_data_spacy(email_body: str, subject: str) -> dict:
    company = None
    position = None
    status = "Pending"  # Default status

    # Use spaCy model to process the email body
    doc = nlp(email_body)

    # Extract entities
    for ent in doc.ents:
        if ent.label_ == "COMPANY":
            company = ent.text
        elif ent.label_ == "POSITION":
            position = ent.text

    # Search for status updates in the email body
    email_body_lower = email_body.lower()
    for update in status_updates:
        if re.search(rf"\b{re.escape(update.lower())}[\s\.\,\!\?]*", email_body_lower):
            # Check if it's a rejection
            if any(re.search(rf"\b{re.escape(rj.lower())}[\s\.\,\!\?]*", email_body_lower) for rj in rejection_keywords):
                status = "Rejected"
            else:
                status = update.capitalize()
            break

    # If no position or company found, check subject as a fallback
    subject_lower = subject.lower()
    if not company:
        doc_subject = nlp(subject)
        for ent in doc_subject.ents:
            if ent.label_ == "COMPANY":
                company = ent.text
    if not position:
        doc_subject = nlp(subject)
        for ent in doc_subject.ents:
            if ent.label_ == "POSITION":
                position = ent.text

    return {"company": company, "position": position, "status": status}

# Test the updated parser
if __name__ == "__main__":
    email_body = """Dear Alec-Nesat Colak, thank you for applying to the Software Engineering I role at Activision. We have received your application and will be in touch shortly."""
    subject = "Your Application to Activision"
    result = parse_email_data_spacy(email_body, subject)
    print(result)
