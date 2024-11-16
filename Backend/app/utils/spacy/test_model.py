import spacy

# Load the saved model
output_dir = "./trained_model"
nlp = spacy.load(output_dir)
print("Model loaded successfully.")

# Sample texts for testing
test_texts = [
    "Dear Alec-Nesat Colak, thank you for applying to the Software Engineering I role at Activision. We have received your application and will be in touch shortly.",
    "Thank you for your interest in joining Microsoft! Your application for Data Scientist has been received.",
    "Dear Alec, we appreciate your application for the Machine Learning Engineer position at Google.",
    "Hi Alec, we are reviewing your application for the Backend Developer role at Amazon and will contact you if you are selected for an interview.",
    "Thank you for applying to Apple for the role of Software Engineer. We look forward to reviewing your application."
]

# Load the saved model
nlp = spacy.load("./trained_model")
print("Model loaded successfully.\n")

# Test the model on each sample text
for i, text in enumerate(test_texts, 1):
    print(f"Test Text {i}: {text}")
    doc = nlp(text)
    
    # Print out the entities recognized by the model
    if doc.ents:
        for ent in doc.ents:
            print(f" - {ent.text}: {ent.label_}")
    else:
        print(" - No entities found.")
    print("-" * 40)  # Separator between texts

