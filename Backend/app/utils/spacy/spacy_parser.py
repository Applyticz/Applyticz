import spacy
import re

# Load spaCy's pre-trained English model
nlp = spacy.load("en_core_web_sm")

# List of common job titles
job_titles = [
    "Software Engineer", "Software Developer", "Data Scientist", "Data Engineer",
    "Project Manager", "Web Developer", "UX Designer", "DevOps Engineer", "Backend Developer",
    "Frontend Developer", "Product Manager", "AI Engineer", "Research Scientist", "QA Engineer", "Junior Software Developer"
]

# Compile a regex pattern from the job titles list for case-insensitive matching
job_titles_pattern = re.compile(r"\b(" + "|".join(re.escape(job) for job in job_titles) + r")\b", re.IGNORECASE)

# Function to clean up job title if it has prefix (like JR1990357)
def clean_job_title(text):
    return re.sub(r"\b\w{2,6}\d+\b\s*", "", text)  # Remove prefix patterns like JR1990357

def extract_company_and_position(email_body, sender_name=""):
    doc = nlp(email_body)
    entities = {
        "company": None,
        "position": None
    }
    
    # Extract company name (first ORG entity or fallback)
    for ent in doc.ents:
        if ent.label_ == "ORG" and not entities["company"]:
            entities["company"] = ent.text  # First organization found is considered the company

    # Fallback for company name if not found by spaCy
    if not entities["company"]:
        # Look for common phrases used to refer to company names
        fallback_pattern = re.compile(r"(Thank you for applying to|at|join us at)\s+([A-Za-z]+)", re.IGNORECASE)
        match = fallback_pattern.search(email_body)
        if match:
            entities["company"] = match.group(2)

    # Extract job title by looking for keywords in the text
    if sender_name:
        sender_name_pattern = re.compile(rf"\b{re.escape(sender_name)}\b", re.IGNORECASE)
        if re.search(sender_name_pattern, email_body):
            entities["position"] = "Unknown"  # Default position if sender's name is found
            return entities

    # Search for job titles in the email body and clean up prefix if present
    for match in re.finditer(job_titles_pattern, email_body):
        entities["position"] = clean_job_title(match.group())
        break  # Stop after finding the first job title

    return entities

# Sample email body
email_body = """Dear Alec-Nesat Colak -

We want to confirm that your application for the JR1990357 AI Software Engineer, Copilots - New College Grad 2024 role has been received.

We are always looking for amazing people to join us in doing their life’s work at NVIDIA, and we’re grateful that you took the time to apply for this opportunity.

We will review your application against the open position, and contact you to arrange an interview if the role is a good match for your qualifications.

Thanks again for your interest in NVIDIA.

Best Regards,

The NVIDIA Recruiting Team"""

sender = "nvidia@myworkday.com"

result = extract_company_and_position(email_body, sender)
print(result)


print(result)


