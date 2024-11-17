import spacy
from spacy.training.example import Example
from spacy.util import minibatch
import random

# Use the corrected TRAIN_DATA
TRAIN_DATA = [
    ("Dear Alec, thank you for your interest in joining Netflix! We appreciate you applying to the position of Data Engineer.",
     {"entities": [(50, 57, "COMPANY"), (105, 118, "POSITION")]}),
    ("Hi Alec-Nesat, Thank you for applying for our Software Engineer Internship 2025 role here at Lucid Software. We have received a great number of applications from many qualified applicants. Although we appreciate your interest in Lucid, at this time you have not been selected to move forward in the hiring process. We have selected candidates whose experience and qualifications are more aligned with our needs at this time. We appreciate the effort you put into applying, and we encourage you to check our job postings regularly. Should there be a position that is of interest to you, we hope you reapply. We wish you the best in your future employment search. Best regards, The Lucid Software Recruiting Team",
     {"entities": [(93, 107, "COMPANY"), (46, 74, "POSITION")]}),
    ("Thank you for Applying! Dear Alec-Nesat , Thank you for your interest in joining Mastercard! Your application for Software Engineer I has been received. We believe in connecting everyone to Priceless possibilities. Your application is the first step in our connection with you. What’s next? You can review our complete hiring process here . Our team is reviewing your application. If your skills and experience are a good fit for this opportunity, you will hear from our talent acquisition team. Regardless of the outcome, we are committed to ensuring that you receive a response regarding your application status. In the meantime, visit our Careers Blog or Mastercard News on YouTube to learn more about our culture, culture playlist and mission to power economies & empower people through critical technology. Interested in applying to other roles? Browse all Mastercard jobs . Thank you, Mastercard Talent Acquisition Take Action Click here to view the notification details. Workday Inbox We're sorry, this email was sent from a mailbox that doesn't accept replies. For more information visit People Place . This email was intended for alecnesatcolak@outlook.com",
     {"entities": [(81, 91, "COMPANY"), (114, 133, "POSITION")]}),
    ("Thank you for applying to Apple for the Machine Learning Engineer role. We will review your application.",
     {"entities": [(26, 31, "COMPANY"), (40, 65, "POSITION")]}),
    ("Alec-Nesat, Thanks for applying to the position of Associate Software Engineer - New Grad (college job board)! You’ve taken an exciting step toward an opportunity like no other. Working here means you get to help change the way businesses connect with their customers and do it with a team that has your back. We work tirelessly to sustain a highly-driven environment built on talent, humility, determination and kindness. We could not be more excited or flattered that you want to be a part of it! Again, a big thank you for applying, and here’s to what’s next in your career! Best Regards, The Sprout Social People Team So what happens next? We’ll review your skills and experience to see if you might be a fit for #TeamSprout. If it’s a match, we will contact you regarding next steps in the process. In the meantime Learn how we work on our careers website. Check out other game-changing roles. Check out our reviews on Glassdoor. Sorry, replies to this message can’t be delivered. Connect with us Sprout Social, 131 S. Dearborn St., Chicago, IL 60603",
     {"entities": [(596, 609, "COMPANY"), (51, 78, "POSITION")]}),
    ("Hi Alec-Nesat, Thank you for applying for the Junior Software Developer in Test position at Global Relay. We really appreciate your interest in joining our team! If your skills and experience are a good fit for the position, a member of our hiring team will contact you to arrange next steps. In the meantime, follow our Instagram account to discover what it’s like to work at Global Relay. Thanks again for your application! Kind regards, Global Relay Recruitment Team Global Relay The leading provider of communications compliance solutions for the global financial sector and other highly regulated industries. Learn more about what it’s like to work at Global Relay here . This is an automated email response. Please do not reply",
     {"entities": [(92, 104, "COMPANY"), (46, 71, "POSITION")]}),
    ("Dear Alec-Nesat, Thank you for your interest in Wave! I'm sure you’re wondering what’s next. Your application will be carefully reviewed by a member of the Talent team and if your experience and skills are a fit for the role, a Recruiter will be in touch. If you don't hear back within three weeks, please be patient with us. Our hiring process typically takes four to six weeks from start to finish, but this is largely dependent on the role and the candidate's availability. We will be in touch as soon as possible. See you soon! Wave Talent Team",
     {"entities": [(48, 52, "COMPANY")]}),
    ("Thank you for applying to NVIDIA for the JR1990357 AI Software Engineer, Copilots - New College Grad 2024 role.",
    {"entities": [(26, 32, "COMPANY"), (51, 71, "POSITION")]}),
    ("Hi Alec, we are reviewing your application for the Backend Developer role at Amazon and will contact you if you are selected for an interview.",
     {"entities": [(77, 83, "COMPANY"), (51, 68, "POSITION")]}),
    ("​Hello Alec-Nesat, Thank you for your interest in launching your career at Visa! We are excited to review your application and will contact you shortly. In the meantime, check out this video on the incredible transformative work Visa has done over the past 60 years! We look forward to connecting with you. Best, Visa’s Early Careers Recruiting Team",
     {"entities": [(75, 79, "COMPANY")]}),
    # Add more training data here
    ("Thank you for applying to Apple for the Machine Learning Engineer role. We will review your application.",
     {"entities": [(26, 31, "COMPANY"), (40, 65, "POSITION")]}),
    ("Hi Alec, we are reviewing your application for the Backend Developer role at Amazon and will contact you if you are selected for an interview.",
     {"entities": [(77, 83, "COMPANY"), (51, 68, "POSITION")]}),
    ("Thank you for submitting your application for the AI Engineer role at Tesla. Our team will review your profile.",
     {"entities": [(70, 75, "COMPANY"), (50, 61, "POSITION")]}),
    ("Dear Alec, your application for the Senior Data Analyst position at SpaceX has been received and is under review.",
     {"entities": [(68, 74, "COMPANY"), (36, 55, "POSITION")]}),
    ("Hi Alec, thank you for your interest in the Software Developer position at Google. We will review your application and get back to you soon.",
     {"entities": [(75, 81, "COMPANY"), (44, 62, "POSITION")]}),
    ("Hello Alec-Nesat, your application for the position of Cloud Architect at AWS has been reviewed.",
     {"entities": [(74, 77, "COMPANY"), (55, 70, "POSITION")]}),
    ("Dear Alec-Nesat, the recruitment team at Facebook is reviewing your application for the Data Engineer role.",
     {"entities": [(41, 49, "COMPANY"), (88, 101, "POSITION")]}),
    ("Greetings Alec, your resume has been received for the Junior UX Designer position at IBM. Thank you for applying!",
     {"entities": [(85, 88, "COMPANY"), (54, 72, "POSITION")]}),
    ("Hi Alec, we are delighted to receive your application for the Senior Machine Learning Engineer role at OpenAI.",
     {"entities": [(103, 109, "COMPANY"), (62, 94, "POSITION")]}),
    ("Hello Alec, thank you for applying to Oracle for the Database Administrator role. We will contact you soon.",
     {"entities": [(38, 44, "COMPANY"), (53, 75, "POSITION")]}),
    ("Dear Alec, your interest in the Software Test Engineer position at Netflix is greatly appreciated. Our hiring team is reviewing your application.",
     {"entities": [(67, 74, "COMPANY"), (32, 54, "POSITION")]}),
    ("Hi Alec, your application for the Cloud Engineer position at Microsoft is currently under review.",
     {"entities": [(61, 70, "COMPANY"), (34, 48, "POSITION")]}),
    ("Hello Alec, our recruitment team at Adobe has received your application for the Frontend Developer role.",
     {"entities": [(36, 41, "COMPANY"), (80, 98, "POSITION")]}),
    ("Greetings Alec-Nesat, thank you for applying to the Junior Software Developer position at IBM.",
     {"entities": [(90, 83, "COMPANY"), (52, 77, "POSITION")]}),
    ("Hello Alec, the HR department at Infinity Ward acknowledges your application for the Senior UX Designer role.",
     {"entities": [(33, 46, "COMPANY"), (85, 103, "POSITION")]}),
    ("Dear Alec, our team at Stitch Fix is reviewing your application for the AI Engineer role.",
     {"entities": [(23, 33, "COMPANY"), (72, 83, "POSITION")]}),
]

# Load a pre-trained English model as a base
nlp = spacy.load("en_core_web_sm")
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")

# Add entity labels to the NER component
for _, annotations in TRAIN_DATA:
    for ent in annotations["entities"]:
        ner.add_label(ent[2])

# Training only the NER component
other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
with nlp.disable_pipes(*other_pipes):
    optimizer = nlp.resume_training()
    
    # Set an early stopping condition
    previous_loss = None
    for i in range(20):  # Training for 20 epochs, but watch for early stopping
        random.shuffle(TRAIN_DATA)
        losses = {}
        # Increase batch size for smoother learning
        batches = minibatch(TRAIN_DATA, size=4)
        for batch in batches:
            for text, annotations in batch:
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                nlp.update([example], drop=0.2, losses=losses)  # Lower drop rate to 0.2
        print("Losses", losses)
        
        # Early stopping check
        current_loss = losses["ner"]
        if previous_loss and abs(previous_loss - current_loss) < 1e-3:  # Threshold for stability
            print(f"Stopping early at epoch {i} due to loss stabilization.")
            break
        previous_loss = current_loss
        
# Save the trained model
output_dir = "./trained_model"
nlp.to_disk(output_dir)
print("Model saved to", output_dir)
