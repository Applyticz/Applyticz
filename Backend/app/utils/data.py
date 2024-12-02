import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, precision_recall_fscore_support
import pandas as pd

SpaCy_predictions =     [{'company': 'SingleStore', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Lucid Software', 'position': 'Unknown', 'status': 'Awaiting Response'},              {'company': 'Unknown', 'position': 'Software Engineering Intern', 'status': 'Awaiting Response'},  {'company': 'Lucid Software', 'position': 'Software Engineer Internship', 'status': 'Rejected'}, {'company': 'Mastercard', 'position': 'Software Engineer I', 'status': 'Awaiting Response'}, {'company': 'Sprout Social', 'position': 'Associate Data Scientist', 'status': 'Awaiting Response'}, {'company': 'Sprout Social', 'position': 'Associate Software Engineer', 'status': 'Awaiting Response'}, {'company': 'Global Relay', 'position': 'Junior Software Developer', 'status': 'Awaiting Response'}, {'company': 'Twilio', 'position': 'Unknown', 'status': 'Awaiting Response'},   {'company': 'Wave', 'position': 'Unknown', 'status': 'Candidate'},         {'company': 'Coalition', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Aurora', 'position': 'Aurora Innovation', 'status': 'Awaiting Response'}, {'company': 'Disney', 'position': 'Software Engineer I.', 'status': 'Candidate'},         {'company': 'Konrad', 'position': 'Software Developer', 'status': 'Interview'},         {'company': 'Unknown', 'position': 'Software Engineer I', 'status': 'Awaiting Response'}, {'company': 'Career Enhancement', 'position': 'Data Engineer', 'status': 'Awaiting Response'}, {'company': 'Unknown', 'position': 'Kikoff Team', 'status': 'Awaiting Response'},      {'company': 'LinkedIn', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Tampa', 'position': 'Terms & Conditions', 'status': 'Awaiting Response'}, {'company': 'Twilio', 'position': 'Software Engineer', 'status': 'Awaiting Response'},   {'company': 'Adobe', 'position': 'Adobe Systems Incorporated', 'status': 'Awaiting Response'}, {'company': 'Unknown', 'position': 'Candidate Account', 'status': 'Interview'},           {'company': 'Unknown', 'position': 'Software Engineer I', 'status': 'Awaiting Response'}, {'company': 'Twitch', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'HashiCorp', 'position': 'Software Engineer I', 'status': 'Awaiting Response'}, {'company': 'LTIMindtree', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Barclays', 'position': 'Test Engineer Barclays Email', 'status': 'Awaiting Response'}]

SpaCy_revised_predictions =  [{'company': 'SingleStore', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Lucid', 'position': 'Unknown', 'status': 'Awaiting Response'},                       {'company': 'Playstation', 'position': 'Software Engineer Intern', 'status': 'Awaiting Response'}, {'company': 'Lucid Software', 'position': 'Software Engineer Internship', 'status': 'Rejected'}, {'company': 'Mastercard', 'position': 'Software Engineer I', 'status': 'Awaiting Response'}, {'company': 'Sprout Social', 'position': 'Associate Data Scientist', 'status': 'Awaiting Response'}, {'company': 'Sprout Social', 'position': 'Associate Software Engineer', 'status': 'Awaiting Response'}, {'company': 'Global Relay', 'position': 'Junior Software Developer', 'status': 'Awaiting Response'}, {'company': 'Twilio', 'position': 'Unknown', 'status': 'Awaiting Response'},   {'company': 'Wave', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Coalition', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Aurora', 'position': 'Aurora Innovation', 'status': 'Awaiting Response'}, {'company': 'Disney', 'position': 'Software Engineer I.', 'status': 'Rejected'},          {'company': 'Konrad', 'position': 'Software Developer', 'status': 'Awaiting Reponse'},  {'company': 'Jamf', 'position': 'Software Engineer I', 'status': 'Awaiting Response'},    {'company': 'USAA', 'position': 'Data Engineer I', 'status': 'Awaiting Response'},             {'company': 'Kikiff', 'position': 'Software Engineer', 'status': 'Awaiting Response'}, {'company': 'LinkedIn', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Dice', 'position': 'Pega Developer', 'status': 'Awaiting Response'},      {'company': 'Twilio', 'position': 'Software Engineer', 'status': 'Awaiting Response'},   {'company': 'Adobe', 'position': 'Adobe Systems Incorporated', 'status': 'Awaiting Response'}, {'company': 'Perseus', 'position': 'Candidate Account', 'status': 'Interview'},           {'company': 'Unknown', 'position': 'Software Engineer I', 'status': 'Awaiting Response'}, {'company': 'Twitch', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'HashiCorp', 'position': 'Software Engineer I', 'status': 'Awaiting Response'}, {'company': 'LTIMindtree', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Barclays', 'position': 'Test Engineer Barclays', 'status': 'Awaiting Response'}]

Hardcoded_predictions = [{'company': 'SingleStore', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Lucid', 'position': 'Unknown', 'status': 'Awaiting Response'},                       {'company': 'Playstation', 'position': 'Software Engineer Intern', 'status': 'Awaiting Response'}, {'company': 'Lucid', 'position': 'Software Engineer', 'status': 'Rejected'},                     {'company': 'Mastercard', 'position': 'Software Engineer', 'status': 'Awaiting Response'},   {'company': 'Sprout Social', 'position': 'Data Scientist', 'status': 'Awaiting Response'},           {'company': 'Sprout Social', 'position': 'Software Engineer', 'status': 'Awaiting Response'},           {'company': 'Global Relay', 'position': 'Software Developer', 'status': 'Awaiting Response'},        {'company': 'LinkedIn', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Wave', 'position': 'Unknown', 'status': 'Candidate'},         {'company': 'Coalition', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'LinkedIn', 'position': 'Unknown', 'status': 'Awaiting Response'},         {'company': 'Disney', 'position': 'Software Engineer', 'status': 'Candidate'},            {'company': 'Konrad', 'position': 'Software Developer', 'status': 'Interview'},         {'company': 'Facebook', 'position': 'Software Engineer', 'status': 'Awaiting Response'},  {'company': 'USAA', 'position': 'Data Engineer', 'status': 'Awaiting Response'},               {'company': 'Kikoff', 'position': 'Software Engineer', 'status': 'Awaiting Response'}, {'company': 'LinkedIn', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Unknown', 'position': 'Unknown', 'status': 'Awaiting Response'},          {'company': 'LinkedIn', 'position': 'Software Engineer', 'status': 'Awaiting Response'}, {'company': 'Twitter', 'position': 'Software Engineer', 'status': 'Awaiting Response'},        {'company': 'Unknown', 'position': 'Software Engineer', 'status': 'Interview'},           {'company': 'Unknown', 'position': 'Software Engineer', 'status': 'Awaiting Response'},   {'company': 'Unknown', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Twitter', 'position': 'Software Engineer', 'status': 'Awaiting Response'},    {'company': 'Unknown', 'position': 'Unknown', 'status': 'Awaiting Response'},     {'company': 'Unknown', 'position': 'Unknown', 'status': 'Awaiting Response'}]

Truth_data =            [{'company': 'SingleStore', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Lucid' , 'position': 'Software Engineer Internship', 'status': 'Awaiting Response'}, {'company': 'Playstation', 'position': 'Software Engineer Intern', 'status': 'Awaiting Response'}, {'company': 'Lucid Software', 'position': 'Software Engineer Internship', 'status': 'Rejected'}, {'company': 'Mastercard', 'position': 'Software Engineer I', 'status': 'Awaiting Response'}, {'company': 'Sprout Social', 'position': 'Associate Data Scientist', 'status': 'Awaiting Response'}, {'company': 'Sprout Social', 'position': 'Associate Software Engineer', 'status': 'Awaiting Response'}, {'company': 'Global Relay', 'position': 'Junior Software Developer', 'status': 'Awaiting Response'}, {'company': 'Twilio', 'position': 'Unknown', 'status': 'Awaiting Response'},   {'company': 'Wave', 'position': 'Unknown', 'status': 'Awaiting Repsonse'}, {'company': 'Coalition', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Aurora', 'position': 'Aurora Innovation', 'status': 'Awaiting Response'}, {'company': 'Disney', 'position': 'Software Engineer I.', 'status': 'Rejected'},          {'company': 'Konrad', 'position': 'Software Developer', 'status': 'Awaiting Response'}, {'company': 'Jamf', 'position': 'Software Engineer I', 'status': 'Awaiting Response'},    {'company': 'USAA', 'position': 'Data Engineer I', 'status': 'Awaiting Response'},             {'company': 'Kikoff', 'position': 'Software Engineer', 'status': 'Awaiting Response'}, {'company': 'LinkedIn', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Dice', 'position': 'Pega Developer', 'status': 'Awaiting Response'},      {'company': 'Twilio', 'position': 'Software Engineer', 'status': 'Awaiting Response'},   {'company': 'Adobe', 'position': 'Software Engineer', 'status': 'Awaiting Response'},          {'company': 'Perseus', 'position': 'Software Engineer I', 'status': 'Awaiting Response'}, {'company': 'Unknown', 'position': 'Software Engineer I', 'status': 'Awaiting Response'}, {'company': 'Twitch', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'HashiCorp', 'position': 'Software Engineer I', 'status': 'Awaiting Response'}, {'company': 'LTIMindtree', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Barclays', 'position': 'Test Engineer Barclays Email', 'status': 'Awaiting Response'}]

# Convert lists to DataFrames
spacy_df = pd.DataFrame(SpaCy_predictions)
spacy_revised_df = pd.DataFrame(SpaCy_revised_predictions)
hardcoded_df = pd.DataFrame(Hardcoded_predictions)
truth_df = pd.DataFrame(Truth_data)

# Helper function to compute metrics
def compute_metrics(predictions, truth, column):
    pred = predictions[column].fillna("Unknown")
    actual = truth[column].fillna("Unknown")
    report = classification_report(actual, pred, output_dict=True, zero_division=0)
    return report

# Compute metrics for each method
spacy_metrics = {
    "status": compute_metrics(spacy_df, truth_df, "status"),
    "company": compute_metrics(spacy_df, truth_df, "company"),
    "position": compute_metrics(spacy_df, truth_df, "position")
}

spacy_revised_metrics = {
    "status": compute_metrics(spacy_revised_df, truth_df, "status"),
    "company": compute_metrics(spacy_revised_df, truth_df, "company"),
    "position": compute_metrics(spacy_revised_df, truth_df, "position")
}

hardcoded_metrics = {
    "status": compute_metrics(hardcoded_df, truth_df, "status"),
    "company": compute_metrics(hardcoded_df, truth_df, "company"),
    "position": compute_metrics(hardcoded_df, truth_df, "position")
}

# Aggregate accuracy for comparison
accuracy_comparison = pd.DataFrame({
    "Field": ["Status", "Company", "Position"],
    "SpaCy Accuracy": [spacy_metrics["status"]["accuracy"], spacy_metrics["company"]["accuracy"], spacy_metrics["position"]["accuracy"]],
    "SpaCy Revised Accuracy": [spacy_revised_metrics["status"]["accuracy"], spacy_revised_metrics["company"]["accuracy"], spacy_revised_metrics["position"]["accuracy"]],
    "Hardcoded Accuracy": [hardcoded_metrics["status"]["accuracy"], hardcoded_metrics["company"]["accuracy"], hardcoded_metrics["position"]["accuracy"]]
})

# Plot accuracy comparison
plt.figure(figsize=(10, 6))
accuracy_comparison.set_index("Field").plot(kind="bar", alpha=0.7)
plt.title("Accuracy Comparison: SpaCy vs SpaCy Revised vs Hardcoded")
plt.ylabel("Accuracy")
plt.xticks(rotation=0)
plt.legend(title="Prediction Source")
plt.grid(axis="y")
plt.show()

# Plot accuracy per category
for field in ["status", "company", "position"]:
    accuracy_data = pd.DataFrame({
        "Method": ["SpaCy", "SpaCy Revised", "Hardcoded"],
        "Accuracy": [
            spacy_metrics[field]["accuracy"],
            spacy_revised_metrics[field]["accuracy"],
            hardcoded_metrics[field]["accuracy"]
        ]
    })
    plt.figure(figsize=(8, 5))
    plt.bar(accuracy_data["Method"], accuracy_data["Accuracy"], color=["blue", "green", "orange"])
    plt.title(f"Accuracy by Method: {field.capitalize()}")
    plt.ylabel("Accuracy")
    plt.ylim(0, 1)
    plt.show()

# Error counts
error_counts = pd.DataFrame({
    "Field": ["Status", "Company", "Position"],
    "SpaCy Errors": [
        len(spacy_df[spacy_df["status"] != truth_df["status"]]),
        len(spacy_df[spacy_df["company"] != truth_df["company"]]),
        len(spacy_df[spacy_df["position"] != truth_df["position"]])
    ],
    "SpaCy Revised Errors": [
        len(spacy_revised_df[spacy_revised_df["status"] != truth_df["status"]]),
        len(spacy_revised_df[spacy_revised_df["company"] != truth_df["company"]]),
        len(spacy_revised_df[spacy_revised_df["position"] != truth_df["position"]])
    ],
    "Hardcoded Errors": [
        len(hardcoded_df[hardcoded_df["status"] != truth_df["status"]]),
        len(hardcoded_df[hardcoded_df["company"] != truth_df["company"]]),
        len(hardcoded_df[hardcoded_df["position"] != truth_df["position"]])
    ]
})

# Plot error counts
plt.figure(figsize=(12, 6))
error_counts.set_index("Field").plot(kind="bar", alpha=0.7)
plt.title("Error Counts by Field: SpaCy vs SpaCy Revised vs Hardcoded")
plt.ylabel("Error Count")
plt.xticks(rotation=0)
plt.legend(title="Prediction Source")
plt.grid(axis="y")
plt.show()

# Overall comparison pie chart
overall_accuracy = pd.DataFrame({
    "Method": ["SpaCy", "SpaCy Revised", "Hardcoded"],
    "Accuracy": [
        accuracy_comparison["SpaCy Accuracy"].mean(),
        accuracy_comparison["SpaCy Revised Accuracy"].mean(),
        accuracy_comparison["Hardcoded Accuracy"].mean()
    ]
})

plt.figure(figsize=(8, 8))
plt.pie(overall_accuracy["Accuracy"], labels=overall_accuracy["Method"], autopct='%1.1f%%', startangle=90)
plt.title("Overall Accuracy Comparison")
plt.axis("equal")
plt.show()

# Data for execution times with differentiation
execution_times = {
    "Endpoint": [
        "Manual (1 phrase)",                   # Normal
        "Spacy (1 phrase)",                       # SpaCy
        "Manual (2 phrase)", # Normal
        "Spacy (2 phrase)",   # SpaCy
        "Manual (3 phrase)", # Normal
        "Spacy (3 phrase)", # SpaCy
        "Manual (4 phrase)", # Normal 
        "Spacy (4 phrase)"# SpaCy
    ],
    "Execution Time (seconds)": [
        0.8170700073242188,
        2.098773956298828,
        2.6362969875335693,
        0.523474931716919,
        2.655405044555664,
        0.45552897453308105,
        2.684836893081665,
        0.4328410339355469
    ]
}

# Create a DataFrame for plotting
execution_df = pd.DataFrame(execution_times)

# Assign colors based on whether the endpoint uses SpaCy or not
colors = ['skyblue' if 'spacy' in endpoint.lower() else 'lightcoral' for endpoint in execution_df["Endpoint"]]

# Plot execution times with color differentiation
plt.figure(figsize=(12, 6))
plt.barh(execution_df["Endpoint"], execution_df["Execution Time (seconds)"], color=colors)
plt.xlabel("Execution Time (seconds)")
plt.title("Execution Time Comparison for API Endpoints")
plt.grid(axis='x')

# Rotate y-axis labels for better visibility
plt.yticks(rotation=30, ha='right')

plt.legend(handles=[plt.Rectangle((0,0),1,1, color='skyblue'), plt.Rectangle((0,0),1,1, color='lightcoral')],
           labels=['SpaCy', 'Normal'], title='Endpoint Type')
plt.show()