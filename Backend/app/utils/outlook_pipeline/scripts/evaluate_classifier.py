# scripts/evaluate_classifier.py

import pandas as pd
import joblib
from sklearn.metrics import classification_report

# Load test data
data = pd.read_csv('../data/processed_emails.csv')
X_test = data['processed_body']
y_test = data['label']

# Load the trained model and vectorizer
model = joblib.load('../models/email_classifier.joblib')
vectorizer = joblib.load('../models/tfidf_vectorizer.joblib')

# Transform test data
X_test_tfidf = vectorizer.transform(X_test)

# Make predictions
predictions = model.predict(X_test_tfidf)

# Evaluate the model
print(classification_report(y_test, predictions))
