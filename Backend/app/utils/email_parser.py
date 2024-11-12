import re

possible_companies = [
    "Google", "Microsoft", "Apple", "Amazon", "Facebook", "Mastercard", "Twitter", "LinkedIn", "Netflix", "Spotify",
    "Uber", "Lyft", "Airbnb", "Slack", "Dropbox", "Salesforce", "Oracle", "IBM", "Intel", "Nvidia",
    "Qualcomm", "Cisco", "HP", "Dell", "Samsung", "Sony", "Panasonic", "LG", "Toshiba", "Nokia",
    "Motorola", "Xerox", "Adobe", "VMware", "PayPal", "Square", "Stripe", "Reddit", "Pinterest",
    "Snapchat", "TikTok", "Zoom", "Epic Games", "Unity", "Riot Games", "Activision", "Blizzard",
    "Sony", "Nintendo", "Sega", "Capcom", "Bandai Namco", "Konami", "Square Enix", "Ubisoft", "Lucid", "Playstation", "SingleStore", "Disney", "Global Relay", "Sprout Social"
]

status_updates = [
    "received", "declined", "rejected", "accepted", "interview", "offer", "candidate", "not been selected", "not selected", "application unsuccessful", "shortlisted", "reviewed", "pending", "in progress", "on hold", "withdrawn", "hired", "onboarding", "completed", "closed", "archived"
]

job_positions = [ "Software Engineer", "Data Scientist", "Product Manager", "UX Designer", "Project Manager", "QA Engineer", "DevOps Engineer", "Web Developer", "Software Engineering Intern", "Data Science Intern", "Product Management Intern", "UX Design Intern", "Project Management Intern", "QA Intern", "DevOps Intern", "Web Development Intern", "Software Engineer", "Software Developer", "Data Scientist", "Data Engineer",
    "Project Manager", "Web Developer", "UX Designer", "DevOps Engineer", "Backend Developer",
    "Frontend Developer", "Product Manager", "AI Engineer", "Research Scientist", "QA Engineer, Junior Software Developer"]

rejection_keywords = [ "not been selected", "not selected", "application unsuccessful", "declined", "rejected" ]


def parse_email_data_hardcoded(email_body, subject ):
    company = None
    position = None
    status = "Unknown"  # Default status

    # Lowercase the email body for case-insensitive matching
    email_body_lower = email_body.lower()
    print(email_body_lower)
    subject_lower = subject.lower()

    # Find the company (stop at first match)
    for c in possible_companies:
        # Use regex to match the company name, allowing for trailing punctuation like !,.?
        if re.search(rf"\b{re.escape(c.lower())}\b", email_body_lower, re.IGNORECASE):
            company = c
            print("Company found: ", company)
            break  # Stop after finding the first matching company

    # If still no company found, check the subject line
    if not company:
        for c in possible_companies:
            if re.search(rf"\b{re.escape(c.lower())}\b", subject_lower, re.IGNORECASE):
                company = c
                break  # Stop after finding the first matching company

    # Search for status updates in the email body
    for update in status_updates:
        # Use regex to match the status, allowing for trailing punctuation
        if re.search(rf"\b{re.escape(update.lower())}[\s\.\,\!\?]*", email_body_lower):
            # If a rejection phrase is found, set status to "Rejected"
            if any(re.search(rf"\b{re.escape(rj.lower())}[\s\.\,\!\?]*", email_body_lower) for rj in rejection_keywords):
                status = "Rejected"
            else:
                status = update.capitalize()  # Default to the status found (e.g., "Rejected")
            break  # Stop after finding the first matching status
        else:
            status = "Pending"  # Default status if no update is found
        
    # Find the job position (stop at first match)
    for pos in job_positions:
        if re.search(rf"\b{re.escape(pos.lower())}[\s\.\,\!\?]*", email_body_lower):
            position = pos
            # if next word is "intern" or "Intern", add it to the position
            if re.search(rf"\bintern\b", email_body_lower):
                position += " Intern"
            break  # Stop after finding the first matching position
        else:
            position = "Unknown"

    return {"company": company, "position": position, "status": status}