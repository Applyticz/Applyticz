import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_fscore_support

# Sample data: Replace with your actual test data and parsing results
test_data = [
    {"text": "Email 1", "company": "Google", "position": "Software Engineer", "status": "Accepted"},
    {"text": "Email 2", "company": "Microsoft", "position": "Data Scientist", "status": "Rejected"},
    # Add more test data
]

# Results from spaCy and manual parsing
spacy_results = [
    {"company": "Amazon", "position": "Software Engineer", "status": "Accepted"},
    {"company": "Microsoft", "position": "Data Scientist", "status": "Rejected"},
    # Add more results
]

manual_results = [
    {"company": "Google", "position": "Software Engineer", "status": "Accepted"},
    {"company": "Microsoft", "position": "Data Scientist", "status": "Rejected"},
    # Add more results
]

# Function to calculate metrics
def calculate_metrics(true_data, predicted_data):
    true_labels = [d['company'] for d in true_data]
    predicted_labels = [d['company'] for d in predicted_data]
    precision, recall, f1, _ = precision_recall_fscore_support(true_labels, predicted_labels, average='weighted')
    return precision, recall, f1

# Calculate metrics
spacy_precision, spacy_recall, spacy_f1 = calculate_metrics(test_data, spacy_results)
manual_precision, manual_recall, manual_f1 = calculate_metrics(test_data, manual_results)

# Create a DataFrame for visualization
metrics_df = pd.DataFrame({
    "Metric": ["Precision", "Recall", "F1 Score"],
    "spaCy": [spacy_precision, spacy_recall, spacy_f1],
    "Manual": [manual_precision, manual_recall, manual_f1]
})

# Plot the metrics
metrics_df.plot(x="Metric", kind="bar", figsize=(10, 6))
plt.title("Comparison of spaCy and Manual Parsing")
plt.ylabel("Score")
plt.ylim(0, 1)
plt.xticks(rotation=0)
plt.legend(loc="lower right")
plt.tight_layout()

# Save the plot to a file
plt.savefig("parsing_accuracy_comparison.png")

# Show the plot
plt.show()