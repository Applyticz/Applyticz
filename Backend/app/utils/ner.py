#from transformers import pipeline

# Load a pre-trained NER pipeline from Hugging Face
#ner_pipeline = pipeline("ner", model="dslim/bert-base-NER")

#def extract_company_and_position_bert(email_body):
#    entities = ner_pipeline(email_body)
#    company, position = None, None#
#    for entity in entities:
#        if entity['entity'] == 'B-ORG' and not company:
#            company = entity['word']
#        elif 'JOB_TITLE' in entity['entity'] and not position:
#            position = entity['word']
#
#    return {"company": company, "position": position}