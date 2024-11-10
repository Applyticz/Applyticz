import pandas as pd

# Data for the CSV file
data = [
    {
        "subject": "Thank you for applying to Twilio!",
        "from_email": "no-reply@twilio.com",
        "receivedDateTime": "2024-11-09T23:43:10Z",
        "body_preview": "Thank you for your interest in a role at Twilio! We just received your application. We know that job hunting can be stressful. Our intention is to be transparent about our hiring process to help you succeed...",
        "body": "Hi Alec-Nesat, Thank you for your interest in a role at Twilio! We just received your application... Thank you, -Twilio Recruiting Team #WeBuildAtTwilio",
        "company": "Twilio",
        "status": "Received",
        "label": 1
    },
    {
        "subject": "Thank you for applying to Global Relay",
        "from_email": "careers@globalrelay.net",
        "receivedDateTime": "2024-11-07T22:59:10Z",
        "body_preview": "Thank you for applying for the Junior Software Developer in Test position at Global Relay. We really appreciate your interest in joining our team!...",
        "body": "Thank you for applying for the Junior Software Developer in Test position at Global Relay. We really appreciate your interest in joining our team...",
        "company": "Global Relay",
        "status": "Pending",
        "label": 1
    },
    {
        "subject": "You Applied to Sprout Social",
        "from_email": "no-reply@us.greenhouse-mail.io",
        "receivedDateTime": "2024-11-07T13:27:09Z",
        "body_preview": "Alec-Nesat, Thanks for applying to the position of Associate Software Engineer - New Grad...",
        "body": "Alec-Nesat, Thanks for applying to the position of Associate Software Engineer - New Grad... Best Regards, The Sprout Social People Team",
        "company": "Sprout Social",
        "status": "Pending",
        "label": 1
    },
    {
        "subject": "Thank You for Applying",
        "from_email": "mastercard@myworkday.com",
        "receivedDateTime": "2024-11-07T03:57:23Z",
        "body_preview": "Thank you for Applying! Dear Alec-Nesat , Thank you for your interest in joining Mastercard! Your application for Software Engineer I has been received...",
        "body": "Thank you for Applying! Dear Alec-Nesat , Thank you for your interest in joining Mastercard...",
        "company": "Mastercard",
        "status": "Received",
        "label": 1
    },
    {
        "subject": "Update about your application to Lucid Software",
        "from_email": "no-reply@us.greenhouse-mail.io",
        "receivedDateTime": "2024-10-23T15:45:15Z",
        "body_preview": "Thank you for applying for our Software Engineer Internship 2025 role here at Lucid Software...",
        "body": "Hi Alec-Nesat, Thank you for applying for our Software Engineer Internship 2025 role here at Lucid Software... Best regards, The Lucid Software Recruiting Team",
        "company": "Lucid",
        "status": "Rejected",
        "label": 1
    },
    {
        "subject": "Interview Invitation from Tech Corp",
        "from_email": "hr@techcorp.com",
        "receivedDateTime": "2024-10-25T15:00:00Z",
        "body_preview": "We are pleased to invite you for an interview for the role of Software Engineer at Tech Corp...",
        "body": "Dear Alec-Nesat, Congratulations! We would like to invite you for an interview for the Software Engineer position at Tech Corp...",
        "company": "Tech Corp",
        "status": "Interviewing",
        "label": 1
    },
    {
        "subject": "Application Rejection Notice",
        "from_email": "hr@bigdata.com",
        "receivedDateTime": "2024-10-22T12:30:00Z",
        "body_preview": "After careful consideration, we have decided to not proceed with your application...",
        "body": "Dear Alec-Nesat, Thank you for applying to Big Data Solutions...",
        "company": "Big Data",
        "status": "Rejected",
        "label": 1
    },
    {
        "subject": "Offer from DataWave",
        "from_email": "careers@datawave.com",
        "receivedDateTime": "2024-10-28T11:00:00Z",
        "body_preview": "We are excited to extend an offer to join us at DataWave as a Data Scientist...",
        "body": "Hi Alec-Nesat, Congratulations! We are thrilled to offer you the Data Scientist position...",
        "company": "DataWave",
        "status": "Offer Accepted",
        "label": 1
    },
    {
        "subject": "Monthly Newsletter",
        "from_email": "news@unrelatednewsletter.com",
        "receivedDateTime": "2024-10-05T12:00:00Z",
        "body_preview": "Here’s the latest from our team at Unrelated Newsletter!...",
        "body": "Hello, here’s what’s new in our latest issue of Unrelated Newsletter!...",
        "company": "Unrelated",
        "status": "N/A",
        "label": 0
    },
    {
        "subject": "Special Offer - Exclusive Savings",
        "from_email": "promo@shoppingdeal.com",
        "receivedDateTime": "2024-09-25T08:00:00Z",
        "body_preview": "Get 30% off on your next purchase with this exclusive offer!...",
        "body": "Hello! Shop now and enjoy exclusive savings on your favorite items!...",
        "company": "Shopping Deal",
        "status": "N/A",
        "label": 0
    },
    {
        "subject": "Interview Invitation from Amazon",
        "from_email": "no-reply@amazon.jobs",
        "receivedDateTime": "2024-11-12T08:30:00Z",
        "body_preview": "We are pleased to invite you for an interview for the Software Engineer position...",
        "body": "Dear Alec-Nesat, We reviewed your application and are excited to invite you to the next stage of the hiring process at Amazon. Your interview for the Software Engineer position is scheduled for...",
        "company": "Amazon",
        "status": "Interviewing",
        "label": 1
    },
    {
        "subject": "Application Update from Google",
        "from_email": "careers@google.com",
        "receivedDateTime": "2024-11-10T14:20:45Z",
        "body_preview": "Thank you for your interest in joining Google. We have carefully reviewed your application...",
        "body": "Hello Alec-Nesat, After careful consideration, we regret to inform you that we have decided to pursue other candidates for the Software Engineer position. We encourage you to apply to other roles that may suit your skills and experience. Best wishes, Google Careers Team.",
        "company": "Google",
        "status": "Rejected",
        "label": 1
    },
    {
        "subject": "Thank you for applying to Netflix",
        "from_email": "jobs@netflix.com",
        "receivedDateTime": "2024-11-08T11:15:00Z",
        "body_preview": "Thank you for your application! We will be in touch if your profile matches our requirements...",
        "body": "Hi Alec-Nesat, Thank you for applying to Netflix! We have received your application for the Software Engineering Internship. Our hiring team is currently reviewing your qualifications and will reach out if there's a fit...",
        "company": "Netflix",
        "status": "Pending",
        "label": 1
    },
    {
        "subject": "Online Assessment Invitation from Microsoft",
        "from_email": "assessment@msft.com",
        "receivedDateTime": "2024-11-15T10:00:00Z",
        "body_preview": "Please complete the online assessment for the Data Analyst position within 7 days...",
        "body": "Dear Alec-Nesat, Congratulations! You have been selected to complete an online assessment for the Data Analyst role at Microsoft. This assessment is an important part of our hiring process and should be completed within 7 days...",
        "company": "Microsoft",
        "status": "Online Assessment",
        "label": 1
    },
    {
        "subject": "Offer from Tesla for Data Engineer Role",
        "from_email": "careers@tesla.com",
        "receivedDateTime": "2024-11-18T09:00:00Z",
        "body_preview": "We are excited to extend an offer to join Tesla as a Data Engineer...",
        "body": "Dear Alec-Nesat, Congratulations! We are thrilled to offer you a position as a Data Engineer at Tesla. Please review the attached offer letter and let us know if you have any questions...",
        "company": "Tesla",
        "status": "Offer Accepted",
        "label": 1
    },
    # Non-application emails
    {
        "subject": "Weekly Tech Insights Newsletter",
        "from_email": "newsletter@techinsights.com",
        "receivedDateTime": "2024-11-01T07:45:00Z",
        "body_preview": "Here's your latest edition of Tech Insights with updates from around the tech world...",
        "body": "Hello Subscriber, Welcome to this week’s Tech Insights! In this issue, we cover the latest trends and innovations...",
        "company": "Tech Insights",
        "status": "N/A",
        "label": 0
    },
    {
        "subject": "New Event Invitation: AI Conference 2024",
        "from_email": "events@aiconference.com",
        "receivedDateTime": "2024-10-29T15:30:00Z",
        "body_preview": "Join us for AI Conference 2024 to learn about the latest in artificial intelligence and machine learning...",
        "body": "Dear Alec-Nesat, We are excited to invite you to the upcoming AI Conference 2024! Register now to reserve your spot...",
        "company": "AI Conference",
        "status": "N/A",
        "label": 0
    },
    {
        "subject": "Your Monthly Bank Statement",
        "from_email": "support@yourbank.com",
        "receivedDateTime": "2024-10-25T18:10:00Z",
        "body_preview": "Your October statement is now available for viewing...",
        "body": "Dear Alec-Nesat, Your bank statement for the month of October is ready. Please log in to your account to view the details...",
        "company": "Your Bank",
        "status": "N/A",
        "label": 0
    },
    {
        "subject": "Thank you for applying to Stripe!",
        "from_email": "no-reply@careers.stripe.com",
        "receivedDateTime": "2024-11-08T16:43:10Z",
        "body_preview": "Hi Alec-Nesat, Thank you so much for your application and interest in Stripe.",
        "body": (
            "Hi Alec-Nesat, Thank you so much for your application and interest in Stripe. We received applications "
            "from many qualified candidates and unfortunately are going in a direction that better fits our needs "
            "at this time. That said, things are constantly evolving at Stripe, and there could be a fit for you "
            "down the road. We encourage you to keep an eye on our jobs page for future opportunities. Thanks again "
            "and we wish you the best in your search! Kindly, Stripe Recruiting."
        ),
        "status": "Rejected",
        "label": 1
    },
    {
        "subject": "Thank you for your interest",
        "from_email": "walmart@myworkday.com",
        "receivedDateTime": "2024-10-20T14:25:12Z",
        "body_preview": "Hi Alec-Nesat, Thank you for your interest.",
        "body": (
            "Hi Alec-Nesat, Thank you for your interest. We appreciate the time you took to apply with us. At this "
            "time we have decided not to move forward with your application for our 2024 Summer Intern: Software "
            "Engineer II (Sam's Club) position. This isn't the end, though! If a position opens that closely matches "
            "your skills and experience, we may contact you as we have new positions that open all the time. We wish "
            "you all the best! Your Sam’s Club Hiring Team."
        ),
        "status": "Rejected",
        "label": 1
    },
    {
        "subject": "Update about your application to Salesforce",
        "from_email": "salesforce@myworkday.com",
        "receivedDateTime": "2024-10-15T11:42:15Z",
        "body_preview": "Hi Alec-Nesat, Thank you for your interest in Salesforce.",
        "body": (
            "Hi Alec-Nesat, Thank you for your interest in Salesforce. We understand the time and effort it takes to "
            "search for a new role and we greatly appreciate you applying. The Software Engineering AMTS/MTS (New "
            "Grad) position has been filled and the job opening is now closed. If you applied for multiple positions, "
            "your other applications may still be moving forward. You can check your application status at any time "
            "via the Candidate Home on Workday. Thanks again for considering Salesforce."
        ),
        "status": "Position Filled",
        "label": "Position Filled"
    },
    {
        "subject": "Thank you for applying to ZipRecruiter",
        "from_email": "no-reply@ziprecruiter.com",
        "receivedDateTime": "2024-10-10T09:38:09Z",
        "body_preview": "Hi Alec-Nesat, Thank you for your interest in our Software Engineer - New Grad role.",
        "body": (
            "Hi Alec-Nesat, Thank you for your interest in our Software Engineer - New Grad role. We really appreciate "
            "the time you took to consider an opportunity with us. After reviewing your application, we have decided "
            "not to move you forward for the Software Engineer - New Grad position at this time. We encourage you to "
            "check out more of our openings at www.ziprecruiter.com/careers."
        ),
        "status": "Rejected",
        "label": 1
    },
    {
        "subject": "Follow-up on your application to Epsilon Systems",
        "from_email": "no-reply@epsilonsystems.com",
        "receivedDateTime": "2024-09-30T08:22:45Z",
        "body_preview": "Dear Alec-Nesat, You are receiving this email because you expressed interest in, and applied to...",
        "body": (
            "Dear Alec-Nesat, You are receiving this email because you expressed interest in, and applied to the "
            "Software Engineer Intern (CEC) opportunity on our CEC Program in Largo FL. We have received overwhelming "
            "interest and as we approach the end of 2024, we are refreshing all of our program requisitions, so that "
            "we can start our next round of interviews. If you are still interested in being considered, please check "
            "our careers page and complete an application for the newly posted internship opportunities."
        ),
        "status": "Pending",
        "label": 1
    },
    {
    "subject": "ZipRecruiter Pre-Screen Reminder",
    "from_email": "no-reply@codesignal.com",
    "receivedDateTime": "2024-09-17T20:00:00Z",
    "body_preview": "Hi Alec-Nesat Colak! This is one last reminder! Your last day to complete the ZipRecruiter Pre-Screen...",
    "body": (
        "Hi Alec-Nesat Colak! This is one last reminder! Your last day to complete the ZipRecruiter Pre-Screen "
        "requested by ZipRecruiter is at 2:32pm PDT on Wednesday, September 18th. After you create a CodeSignal "
        "account, you will have access to a practice environment where you can explore CodeSignal’s IDE and different "
        "types of questions before your assessment."
    ),
    "status": "Pre-Screen",
    "label": 1
},
{
    "subject": "Regarding your application to MLH Fellowship",
    "from_email": "fellowship@mlh.io",
    "receivedDateTime": "2024-08-30T15:00:00Z",
    "body_preview": "Hey, there -- Thank you for taking the time to apply for the MLH Fellowship Program. Unfortunately...",
    "body": (
        "Hey, there -- Thank you for taking the time to apply for the MLH Fellowship Program. Unfortunately, after "
        "careful review, we have decided not to proceed with your application. We hope that you'll apply again for a "
        "future batch with an even stronger application!"
    ),
    "status": "Rejected",
    "label": 1
},
{
    "subject": "Your Year Up Eligibility",
    "from_email": "jfowler@yearup.org",
    "receivedDateTime": "2024-09-15T10:00:00Z",
    "body_preview": "Dear Alec-Nesat, Thank you for your interest in the Year Up program. We have received your application...",
    "body": (
        "Dear Alec-Nesat, Thank you for your interest in the Year Up program. We have received your application and "
        "determined you are ineligible for the program. At this time, we have closed your application. To search for "
        "additional programs, we recommend this website sponsored by the US Department of Labor."
    ),
    "status": "Ineligible",
    "label": 1
},
{
    "subject": "Follow-up on your application to Signify Health",
    "from_email": "no-reply@us.greenhouse-mail.io",
    "receivedDateTime": "2024-10-02T11:00:00Z",
    "body_preview": "Alec-Nesat, Thank you for taking the time to apply to the Software Engineer role at Signify Health...",
    "body": (
        "Alec-Nesat, Thank you for taking the time to apply to the Software Engineer role at Signify Health. We received "
        "many qualified candidates and have decided to move forward with another one that we feel is better suited to "
        "our current needs."
    ),
    "status": "Rejected",
    "label": 1
},
{
    "subject": "Thank you for applying to OKX",
    "from_email": "no-reply@us.greenhouse-mail.io",
    "receivedDateTime": "2024-10-05T13:20:00Z",
    "body_preview": "Hi Alec-Nesat, Thanks for applying to OKX for the position Software Engineer, New Grad. We are pleased...",
    "body": (
        "Hi Alec-Nesat, Thanks for applying to OKX for the position Software Engineer, New Grad. We are pleased to confirm "
        "we have received your application and will contact you soon if there is a fit."
    ),
    "status": "Received",
    "label": 1
},
{
    "subject": "Application Confirmation from Signify Health",
    "from_email": "no-reply@us.greenhouse-mail.io",
    "receivedDateTime": "2024-10-06T09:30:00Z",
    "body_preview": "Alec-Nesat, Thanks for applying to Signify Health. Your application has been received...",
    "body": (
        "Alec-Nesat, Thanks for applying to Signify Health. Your application has been received. Our team will follow up if "
        "there is a match for a phone screen."
    ),
    "status": "Received",
    "label": 1
},
{
    "subject": "Thank you for applying to Year Up",
    "from_email": "applications@yearup.org",
    "receivedDateTime": "2024-09-05T15:00:00Z",
    "body_preview": "Hi Alec-Nesat, Thank you for your application to the Year Up program...",
    "body": (
        "Hi Alec-Nesat, Thank you for your application to the Year Up program. We are currently reviewing applications and "
        "will notify you if you advance to the next stage."
    ),
    "status": "Pending",
    "label": 1
},
{
    "subject": "Interview Scheduled with Salesforce",
    "from_email": "recruiting@salesforce.com",
    "receivedDateTime": "2024-10-10T14:00:00Z",
    "body_preview": "Hi Alec-Nesat, We’re excited to invite you to an interview for the Software Engineering role...",
    "body": (
        "Hi Alec-Nesat, We’re excited to invite you to an interview for the Software Engineering role at Salesforce. "
        "Please confirm your availability and review our interview preparation materials."
    ),
    "status": "Interviewing",
    "label": 1
},
{
    "subject": "Update on Your Application Status - Year Up",
    "from_email": "noreply@yearup.org",
    "receivedDateTime": "2024-10-15T08:00:00Z",
    "body_preview": "Dear Alec-Nesat, We are writing to inform you about your application to the Year Up program...",
    "body": (
        "Dear Alec-Nesat, We are writing to inform you about your application to the Year Up program. Unfortunately, "
        "we are unable to move forward with your application at this time. We encourage you to reapply in the future."
    ),
    "status": "Rejected",
    "label": 1
},
{
    "subject": "Assessment Reminder from CodeSignal",
    "from_email": "no-reply@codesignal.com",
    "receivedDateTime": "2024-11-02T17:00:00Z",
    "body_preview": "Hi Alec-Nesat, This is a reminder to complete your assessment for the Software Engineer role...",
    "body": (
        "Hi Alec-Nesat, This is a reminder to complete your assessment for the Software Engineer role. You can log into "
        "CodeSignal to complete it at your convenience before the deadline."
    ),
    "status": "Assessment",
    "label": 1
}
    
]

# Create DataFrame
df = pd.DataFrame(data)

# Save as CSV file
output_path = "application_emails.csv"
df.to_csv(output_path, index=False)

output_path
