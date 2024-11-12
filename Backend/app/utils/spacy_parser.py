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

# List of terms to avoid as companies, like user's name or common names
exclude_terms = {"alec-nesat", "alec", "nesat"}

def extract_company_and_position(email_body, sender_name=""):
    doc = nlp(email_body)
    entities = {
        "company": None,
        "position": None
    }

    # First, try to use sender information as the company name if available and valid
    sender_name_cleaned = sender_name.lower().strip()
    if sender_name_cleaned and sender_name_cleaned not in exclude_terms:
        entities["company"] = sender_name

    # Extract company name (first valid ORG entity if sender_name doesn't work)
    for ent in doc.ents:
        if ent.label_ == "ORG" and not entities["company"]:
            org_name = ent.text.lower()
            if org_name not in exclude_terms:
                entities["company"] = ent.text  # Set company name if it doesn’t match exclude list
                break

    # Extract job title using regex search
    position_match = job_titles_pattern.search(email_body)
    if position_match:
        entities["position"] = position_match.group()

    return entities

# Example usage
email_body = """
Alec-Nesat,

Thank you for your recent interest in working with Sprout Social! We’ve had a tremendous response to our Associate Data Scientist - New Grad posting and are in the difficult position of having to say no to many people like you who undoubtedly have much to offer.
"""
sender_name = "Sprout Social"
result = extract_company_and_position(email_body, sender_name)
print(result)
