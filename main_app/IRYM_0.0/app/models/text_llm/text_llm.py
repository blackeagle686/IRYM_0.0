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
import torch

# Constants
CSV_FILE = "../datasets/prompt_recommendations.csv"
OUTPUT_DIR = "./llm_finetuned2"
MODEL_NAME = "microsoft/phi-2"

class LLMTrainer:
    def __init__(self, model_name=MODEL_NAME):
        os.environ["WANDB_DISABLED"] = "true"

        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

        # Padding fix for Phi-2
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model.config.pad_token_id = self.tokenizer.eos_token_id

    def load_dataset(self, csv_path):
        df = pd.read_csv(csv_path)
        df = df[['Prompt', "Recommendation"]]
        dataset = Dataset.from_pandas(df)
        return dataset

    def format_and_tokenize(self, example):
        text = f"<|prompt|>{example['Prompt']}<|response|>{example['Recommendation']}"
        tokens = self.tokenizer(
            text,
            truncation=True,
            padding="max_length",
            max_length=256  # Increased for larger JSONs
        )
        tokens["labels"] = tokens["input_ids"].copy()
        return tokens

    def train(self, dataset_path, output_dir=OUTPUT_DIR, batch_size=4, epochs=4):
        raw_dataset = self.load_dataset(dataset_path)
        tokenized_dataset = raw_dataset.map(self.format_and_tokenize)

        training_args = TrainingArguments(
            output_dir=output_dir,
            run_name="json_finetune_run",
            per_device_train_batch_size=batch_size,
            num_train_epochs=epochs,
            logging_steps=50,
            save_strategy="no",
            fp16=torch.cuda.is_available(),  # Automatically use FP16 if GPU is available
            report_to="none"
        )

        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_dataset
        )

        trainer.train()

        # Save fine-tuned model and tokenizer
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)
        print(f"\n Model and tokenizer saved to: {output_dir}")


# ===== Run training =====
if __name__ == "__main__":
    trainer = LLMTrainer()
    trainer.train(dataset_path=CSV_FILE)
