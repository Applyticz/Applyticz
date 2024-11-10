# scripts/preprocess.py

import spacy
import pandas as pd

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """
    Tokenizes, removes stop words, punctuation, and lemmatizes text.
    """
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc if not token.is_stop and not token.is_punct])

def preprocess_emails(csv_path, output_path):
    # Load data
    data = pd.read_csv(csv_path)
    
    # Preprocess email bodies
    data['processed_body'] = data['body'].apply(preprocess_text)
    
    # Save to new CSV
    data.to_csv(output_path, index=False)

if __name__ == "__main__":
    preprocess_emails('../data/emails.csv', '../data/processed_emails.csv')
