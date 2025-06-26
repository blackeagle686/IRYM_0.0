# main_app/llm_trainer.py

import os
import pandas as pd
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer
)

class LLMTrainer:
    def __init__(self, model_name="distilgpt2"):
        os.environ["WANDB_DISABLED"] = "true"
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

        # Fix padding
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model.config.pad_token_id = self.tokenizer.eos_token_id

    def load_dataset(self, csv_path):
        df = pd.read_csv(csv_path)
        dataset = Dataset.from_pandas(df)
        return dataset

    def format_and_tokenize(self, example):
        text = f"<|prompt|>{example['prompt']}<|response|>{example['response']}"
        tokens = self.tokenizer(text, truncation=True, padding="max_length", max_length=128)
        tokens["labels"] = tokens["input_ids"].copy()
        return tokens

    def train(self, dataset_path, output_dir="./llm_finetuned", batch_size=4, epochs=4):
        raw_dataset = self.load_dataset(dataset_path)
        tokenized_dataset = raw_dataset.map(self.format_and_tokenize)

        training_args = TrainingArguments(
            output_dir=output_dir,
            run_name="debug_run",
            per_device_train_batch_size=batch_size,
            num_train_epochs=epochs,
            logging_steps=10,
            fp16=True  # GPU only
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_dataset
        )

        trainer.train()

        # Save fine-tuned model
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)
        print(f"✅ Model saved to: {output_dir}")
