import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, precision_recall_fscore_support
import pandas as pd

SpaCy_predictions =     [{'company': 'SingleStore', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Lucid Software', 'position': 'Unknown', 'status': 'Awaiting Response'},              {'company': 'Unknown', 'position': 'Software Engineering Intern', 'status': 'Awaiting Response'},  {'company': 'Lucid Software', 'position': 'Software Engineer Internship', 'status': 'Rejected'}, {'company': 'Mastercard', 'position': 'Software Engineer I', 'status': 'Awaiting Response'}, {'company': 'Sprout Social', 'position': 'Associate Data Scientist', 'status': 'Awaiting Response'}, {'company': 'Sprout Social', 'position': 'Associate Software Engineer', 'status': 'Awaiting Response'}, {'company': 'Global Relay', 'position': 'Junior Software Developer', 'status': 'Awaiting Response'}, {'company': 'Twilio', 'position': 'Unknown', 'status': 'Awaiting Response'},   {'company': 'Wave', 'position': 'Unknown', 'status': 'Candidate'},         {'company': 'Coalition', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Aurora', 'position': 'Aurora Innovation', 'status': 'Awaiting Response'}, {'company': 'Disney', 'position': 'Software Engineer I.', 'status': 'Candidate'},         {'company': 'Konrad', 'position': 'Software Developer', 'status': 'Interview'},         {'company': 'Unknown', 'position': 'Software Engineer I', 'status': 'Awaiting Response'}, {'company': 'Career Enhancement', 'position': 'Data Engineer', 'status': 'Awaiting Response'}, {'company': 'Unknown', 'position': 'Kikoff Team', 'status': 'Awaiting Response'},      {'company': 'LinkedIn', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Tampa', 'position': 'Terms & Conditions', 'status': 'Awaiting Response'}, {'company': 'Twilio', 'position': 'Software Engineer', 'status': 'Awaiting Response'},   {'company': 'Adobe', 'position': 'Adobe Systems Incorporated', 'status': 'Awaiting Response'}, {'company': 'Unknown', 'position': 'Candidate Account', 'status': 'Interview'},           {'company': 'Unknown', 'position': 'Software Engineer I', 'status': 'Awaiting Response'}, {'company': 'Twitch', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'HashiCorp', 'position': 'Software Engineer I', 'status': 'Awaiting Response'}, {'company': 'LTIMindtree', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Barclays', 'position': 'Test Engineer Barclays Email', 'status': 'Awaiting Response'}]

Hardcoded_predictions = [{'company': 'SingleStore', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Lucid', 'position': 'Unknown', 'status': 'Awaiting Response'},                       {'company': 'Playstation', 'position': 'Software Engineer Intern', 'status': 'Awaiting Response'}, {'company': 'Lucid', 'position': 'Software Engineer', 'status': 'Rejected'},                     {'company': 'Mastercard', 'position': 'Software Engineer', 'status': 'Awaiting Response'},   {'company': 'Sprout Social', 'position': 'Data Scientist', 'status': 'Awaiting Response'},           {'company': 'Sprout Social', 'position': 'Software Engineer', 'status': 'Awaiting Response'},           {'company': 'Global Relay', 'position': 'Software Developer', 'status': 'Awaiting Response'},        {'company': 'LinkedIn', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Wave', 'position': 'Unknown', 'status': 'Candidate'},         {'company': 'Coalition', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'LinkedIn', 'position': 'Unknown', 'status': 'Awaiting Response'},         {'company': 'Disney', 'position': 'Software Engineer', 'status': 'Candidate'},            {'company': 'Konrad', 'position': 'Software Developer', 'status': 'Interview'},         {'company': 'Facebook', 'position': 'Software Engineer', 'status': 'Awaiting Response'},  {'company': 'USAA', 'position': 'Data Engineer', 'status': 'Awaiting Response'},               {'company': 'Kikoff', 'position': 'Software Engineer', 'status': 'Awaiting Response'}, {'company': 'LinkedIn', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Unknown', 'position': 'Unknown', 'status': 'Awaiting Response'},          {'company': 'LinkedIn', 'position': 'Software Engineer', 'status': 'Awaiting Response'}, {'company': 'Twitter', 'position': 'Software Engineer', 'status': 'Awaiting Response'},        {'company': 'Unknown', 'position': 'Software Engineer', 'status': 'Interview'},           {'company': 'Unknown', 'position': 'Software Engineer', 'status': 'Awaiting Response'},   {'company': 'Unknown', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Twitter', 'position': 'Software Engineer', 'status': 'Awaiting Response'},    {'company': 'Unknown', 'position': 'Unknown', 'status': 'Awaiting Response'},     {'company': 'Unknown', 'position': 'Unknown', 'status': 'Awaiting Response'}]

Truth_data =            [{'company': 'SingleStore', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Lucid' , 'position': 'Software Engineer Internship', 'status': 'Awaiting Response'}, {'company': 'Playstation', 'position': 'Software Engineer Intern', 'status': 'Awaiting Response'}, {'company': 'Lucid Software', 'position': 'Software Engineer Internship', 'status': 'Rejected'}, {'company': 'Mastercard', 'position': 'Software Engineer I', 'status': 'Awaiting Response'}, {'company': 'Sprout Social', 'position': 'Associate Data Scientist', 'status': 'Awaiting Response'}, {'company': 'Sprout Social', 'position': 'Associate Software Engineer', 'status': 'Awaiting Response'}, {'company': 'Global Relay', 'position': 'Junior Software Developer', 'status': 'Awaiting Response'}, {'company': 'Twilio', 'position': 'Unknown', 'status': 'Awaiting Response'},   {'company': 'Wave', 'position': 'Unknown', 'status': 'Awaiting Repsonse'}, {'company': 'Coalition', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Aurora', 'position': 'Aurora Innovation', 'status': 'Awaiting Response'}, {'company': 'Disney', 'position': 'Software Engineer I.', 'status': 'Rejected'},          {'company': 'Konrad', 'position': 'Software Developer', 'status': 'Awaiting Response'}, {'company': 'Jamf', 'position': 'Software Engineer I', 'status': 'Awaiting Response'},    {'company': 'USAA', 'position': 'Data Engineer I', 'status': 'Awaiting Response'},             {'company': 'Kikoff', 'position': 'Software Engineer', 'status': 'Awaiting Response'}, {'company': 'LinkedIn', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Dice', 'position': 'Pega Developer', 'status': 'Awaiting Response'},      {'company': 'Twilio', 'position': 'Software Engineer', 'status': 'Awaiting Response'},   {'company': 'Adobe', 'position': 'Software Engineer', 'status': 'Awaiting Response'},          {'company': 'Perseus', 'position': 'Software Engineer I', 'status': 'Awaiting Response'}, {'company': 'Unknown', 'position': 'Software Engineer I', 'status': 'Awaiting Response'}, {'company': 'Twitch', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'HashiCorp', 'position': 'Software Engineer I', 'status': 'Awaiting Response'}, {'company': 'LTIMindtree', 'position': 'Unknown', 'status': 'Awaiting Response'}, {'company': 'Barclays', 'position': 'Test Engineer Barclays Email', 'status': 'Awaiting Response'}]


# Convert lists to DataFrames
spacy_df = pd.DataFrame(SpaCy_predictions)
hardcoded_df = pd.DataFrame(Hardcoded_predictions)
truth_df = pd.DataFrame(Truth_data)

# Helper function to compute metrics
def compute_metrics(predictions, truth, column):
    pred = predictions[column].fillna("Unknown")
    actual = truth[column].fillna("Unknown")
    report = classification_report(actual, pred, output_dict=True, zero_division=0)
    return report

# Compute metrics for SpaCy predictions
spacy_status_metrics = compute_metrics(spacy_df, truth_df, "status")
spacy_company_metrics = compute_metrics(spacy_df, truth_df, "company")
spacy_position_metrics = compute_metrics(spacy_df, truth_df, "position")

# Compute metrics for hardcoded predictions
hardcoded_status_metrics = compute_metrics(hardcoded_df, truth_df, "status")
hardcoded_company_metrics = compute_metrics(hardcoded_df, truth_df, "company")
hardcoded_position_metrics = compute_metrics(hardcoded_df, truth_df, "position")

# Prepare data for accuracy comparison
accuracy_comparison_data = {
    "Field": ["Status", "Company", "Position"],
    "SpaCy Accuracy": [
        spacy_status_metrics["accuracy"],
        spacy_company_metrics["accuracy"],
        spacy_position_metrics["accuracy"]
    ],
    "Hardcoded Accuracy": [
        hardcoded_status_metrics["accuracy"],
        hardcoded_company_metrics["accuracy"],
        hardcoded_position_metrics["accuracy"]
    ],
    "Truth Accuracy": [
        1.0,  # Assuming truth data is 100% accurate
        1.0,  # Assuming truth data is 100% accurate
        1.0   # Assuming truth data is 100% accurate
    ],
}
accuracy_comparison_df = pd.DataFrame(accuracy_comparison_data)

# Plot accuracy comparison as a line plot
plt.figure(figsize=(10, 6))
for column in accuracy_comparison_df.columns[1:]:
    plt.plot(accuracy_comparison_df["Field"], accuracy_comparison_df[column], marker='o', label=column)
plt.title("Accuracy Comparison: SpaCy vs Hardcoded vs Truth Data")
plt.ylabel("Accuracy")
plt.ylim(0, 1)
plt.xticks(rotation=0)
plt.legend(title="Prediction Source")
plt.grid()
plt.show()

# Plot overall accuracy as a pie chart
overall_accuracy_data = {
    "Source": ["SpaCy", "Hardcoded"],
    "Accuracy": [
        accuracy_comparison_df["SpaCy Accuracy"].mean(),
        accuracy_comparison_df["Hardcoded Accuracy"].mean()
    ]
}
overall_accuracy_df = pd.DataFrame(overall_accuracy_data)

plt.figure(figsize=(8, 8))
plt.pie(overall_accuracy_df["Accuracy"], labels=overall_accuracy_df["Source"], autopct='%1.1f%%', startangle=90)
plt.title("Overall Accuracy Comparison: SpaCy vs Hardcoded")
plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
plt.show()

# Compare distributions of status predictions
spacy_status_counts = spacy_df["status"].value_counts()
truth_status_counts = truth_df["status"].value_counts()

# Plot distribution of status predictions
plt.figure(figsize=(10, 6))
spacy_status_counts.plot(kind="bar", alpha=0.7, label="SpaCy Predictions", color="blue")
truth_status_counts.plot(kind="bar", alpha=0.7, label="Truth Data", color="orange")
plt.title("Comparison of Status Predictions")
plt.xlabel("Status")
plt.ylabel("Count")
plt.legend()
plt.show()

# Plot accuracy for each field
accuracy_data = {
    "Field": ["Status", "Company", "Position"],
    "Accuracy": [
        spacy_status_metrics["accuracy"],
        spacy_company_metrics["accuracy"],
        spacy_position_metrics["accuracy"]
    ],
}
accuracy_df = pd.DataFrame(accuracy_data)

plt.figure(figsize=(8, 5))
plt.bar(accuracy_df["Field"], accuracy_df["Accuracy"], color="green")
plt.title("Prediction Accuracy by Field")
plt.ylabel("Accuracy")
plt.ylim(0, 1)
plt.show()

# Identify errors for SpaCy predictions
spacy_errors_df = spacy_df.copy()
spacy_errors_df["truth_status"] = truth_df["status"]
spacy_errors_df["truth_company"] = truth_df["company"]
spacy_errors_df["truth_position"] = truth_df["position"]
spacy_errors_df = spacy_errors_df[
    (spacy_errors_df["status"] != spacy_errors_df["truth_status"])
    | (spacy_errors_df["company"] != spacy_errors_df["truth_company"])
    | (spacy_errors_df["position"] != spacy_errors_df["truth_position"])
]

# Identify errors for hardcoded predictions
hardcoded_errors_df = hardcoded_df.copy()
hardcoded_errors_df["truth_status"] = truth_df["status"]
hardcoded_errors_df["truth_company"] = truth_df["company"]
hardcoded_errors_df["truth_position"] = truth_df["position"]
hardcoded_errors_df = hardcoded_errors_df[
    (hardcoded_errors_df["status"] != hardcoded_errors_df["truth_status"])
    | (hardcoded_errors_df["company"] != hardcoded_errors_df["truth_company"])
    | (hardcoded_errors_df["position"] != hardcoded_errors_df["truth_position"])
]

# Prepare data for error counts and metrics
error_counts = {
    "Field": ["Status", "Company", "Position"],
    "SpaCy Errors": [
        (spacy_errors_df["status"] != spacy_errors_df["truth_status"]).sum(),
        (spacy_errors_df["company"] != spacy_errors_df["truth_company"]).sum(),
        (spacy_errors_df["position"] != spacy_errors_df["truth_position"]).sum(),
    ],
    "Hardcoded Errors": [
        (hardcoded_errors_df["status"] != hardcoded_errors_df["truth_status"]).sum(),
        (hardcoded_errors_df["company"] != hardcoded_errors_df["truth_company"]).sum(),
        (hardcoded_errors_df["position"] != hardcoded_errors_df["truth_position"]).sum(),
    ],
    "SpaCy Precision": [
        spacy_status_metrics["precision"],
        spacy_company_metrics["precision"],
        spacy_position_metrics["precision"],
    ],
    "Hardcoded Precision": [
        hardcoded_status_metrics["precision"],
        hardcoded_company_metrics["precision"],
        hardcoded_position_metrics["precision"],
    ],
    "SpaCy Recall": [
        spacy_status_metrics["recall"],
        spacy_company_metrics["recall"],
        spacy_position_metrics["recall"],
    ],
    "Hardcoded Recall": [
        hardcoded_status_metrics["recall"],
        hardcoded_company_metrics["recall"],
        hardcoded_position_metrics["recall"],
    ],
    "SpaCy F1-Score": [
        spacy_status_metrics["f1-score"],
        spacy_company_metrics["f1-score"],
        spacy_position_metrics["f1-score"],
    ],
    "Hardcoded F1-Score": [
        hardcoded_status_metrics["f1-score"],
        hardcoded_company_metrics["f1-score"],
        hardcoded_position_metrics["f1-score"],
    ],
}
error_counts_df = pd.DataFrame(error_counts)

# Plot the count of errors and metrics by field
plt.figure(figsize=(12, 6))
error_counts_df.set_index("Field").plot(kind="bar", alpha=0.7)
plt.title("Errors and Metrics by Field: SpaCy vs Hardcoded Predictions")
plt.ylabel("Count / Score")
plt.xticks(rotation=0)
plt.legend(title="Metrics / Prediction Source")
plt.show()
