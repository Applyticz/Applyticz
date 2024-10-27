# import spacy
import spacy

nlp = spacy.load('en_core_web_sm')

# Function to extract company names and job positions
def extract_company_and_position(email_body):
    doc = nlp(email_body)
    entities = {
        "company": None,
        "position": None
    }
    
    # Extract organizations (companies) and person names (can represent job titles)
    for ent in doc.ents:
        if ent.label_ == "ORG" and not entities["company"]:
            entities["company"] = ent.text  # First organization found is considered the company
        elif ent.label_ == "PERSON" and not entities["position"]:
            entities["position"] = ent.text  # First person found is considered the job title
    
    return entities
