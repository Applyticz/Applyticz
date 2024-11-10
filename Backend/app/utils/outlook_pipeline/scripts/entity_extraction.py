import spacy

nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    entities = {"company": "", "position": "", "status": ""}
    for ent in doc.ents:
        if ent.label_ == "ORG":
            entities["company"] = ent.text
        elif ent.label_ == "JOB_TITLE":  # Custom label if fine-tuned
            entities["position"] = ent.text
        elif ent.label_ == "STATUS":  # Custom label if fine-tuned
            entities["status"] = ent.text
    return entities
