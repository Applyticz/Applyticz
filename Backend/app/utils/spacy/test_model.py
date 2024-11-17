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
    "Thank you for applying to Apple for the role of Software Engineer. We look forward to reviewing your application.",
    "Greetings Alec-Nesat, we have received your application for the Data Engineer position at Facebook. We will review your qualifications and get back to you soon.",
    "Hello Alec, we appreciate your interest in working with DataDog. We will be reviewing your application for the Software Developer role. You should hear from us soon.",
    # Tricky or complex examples
    "Hey Alec, thanks for applying to Tesla for the AI Specialist position! We’re excited to explore how your skills align with our team.",
    "Dear Alec, the recruitment team at SpaceX is thrilled to receive your application for the Senior Data Analyst role.",
    "Hi Alec, we regret to inform you that the position of Cloud Architect at AWS has already been filled. We encourage you to apply for other roles.",
    "Hello Alec, regarding your recent application, we are pleased to inform you that the position of Security Engineer at Cisco is still open.",
    "Dear Alec-Nesat, our hiring team at Oracle has received your resume for the position of Database Administrator. Thank you for applying!",
    "Greetings Alec, your interest in Netflix is highly appreciated. The Software Test Engineer position is currently under review.",
    "Hi Alec-Nesat, the HR department at IBM acknowledges your application for the Junior Software Developer role. We'll get back to you shortly.",
    "Dear Alec, your application for the Senior UX Designer role at Adobe has been reviewed. We'll reach out if we proceed with your candidacy."
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

