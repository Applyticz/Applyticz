# scripts/train_classifier.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load preprocessed data
data = pd.read_csv('../data/processed_emails.csv')

# Split data
X = data['processed_body']
y = data['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorize text using TF-IDF
vectorizer = TfidfVectorizer(max_features=3000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train the classifier
model = RandomForestClassifier()
model.fit(X_train_tfidf, y_train)

# Save the trained model and vectorizer
joblib.dump(model, '../models/email_classifier.joblib')
joblib.dump(vectorizer, '../models/tfidf_vectorizer.joblib')

# Evaluate the model on the test set
predictions = model.predict(X_test_tfidf)
print(classification_report(y_test, predictions))
