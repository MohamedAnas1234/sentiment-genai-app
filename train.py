"""
Sentiment Analysis GPU Training Script
This script demonstrates how to fine-tune a Hugging Face Transformer model for sentiment analysis using a GPU.
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import load_dataset

def main():
    # 1. Setup Device (Use GPU if available)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training on device: {device}")

    # 2. Load Model and Tokenizer
    model_name = "distilbert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    model.to(device)

    # 3. Load Dataset (IMDB movie reviews as an example)
    print("Loading dataset...")
    dataset = load_dataset("imdb")

    # 4. Tokenize Dataset
    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True)

    print("Tokenizing dataset...")
    tokenized_datasets = dataset.map(tokenize_function, batched=True)
    
    # Format for PyTorch
    tokenized_datasets.set_format("torch")
    
    # Create smaller subsets for faster training demonstration
    small_train_dataset = tokenized_datasets["train"].shuffle(seed=42).select(range(1000))
    small_eval_dataset = tokenized_datasets["test"].shuffle(seed=42).select(range(500))

    # 5. Define Training Arguments
    training_args = TrainingArguments(
        output_dir="./results",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        fp16=torch.cuda.is_available(), # Enable mixed precision if using GPU
    )

    # 6. Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=small_train_dataset,
        eval_dataset=small_eval_dataset,
    )

    # 7. Train Model
    print("Starting training...")
    trainer.train()
    
    # 8. Save final model
    print("Saving fine-tuned model...")
    trainer.save_model("./fine_tuned_sentiment_model")
    tokenizer.save_pretrained("./fine_tuned_sentiment_model")
    print("Training complete!")

if __name__ == "__main__":
    main()
