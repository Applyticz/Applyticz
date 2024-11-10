from transformers import DistilBertTokenizer, DistilBertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
import torch

def train_classifier(data, labels):
    tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')

    # Tokenize data
    encodings = tokenizer(data, truncation=True, padding=True)
    labels = torch.tensor(labels)

    # Set up training arguments
    training_args = TrainingArguments(output_dir='./models', num_train_epochs=3, per_device_train_batch_size=8)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=encodings,
        eval_dataset=encodings
    )
    trainer.train()
    return model

def keyword_fallback(text):
    keywords = {
        "rejected": ["rejected", "declined"],
        "interview": ["interview", "screening"],
        "offer": ["offered", "accepted"],
        # Add more status-related keywords as needed
    }
    for key, words in keywords.items():
        if any(word in text.lower() for word in words):
            return key
    return "pending"
