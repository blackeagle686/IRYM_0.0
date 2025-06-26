# main_app/llm_responder.py

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
MODEL_PATH = "./llm_finetuned"  # Replace with the actual path to your model
class LLMResponder:
    def __init__(self, model_path=MODEL_PATH):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)

        # Fix padding
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model.config.pad_token_id = self.tokenizer.eos_token_id

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    def generate_response(self, prompt, max_new_tokens=50):
        input_text = f"<|prompt|>{prompt}<|response|>"
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt").to(self.device)

        with torch.no_grad():
            output = self.model.generate(
                input_ids,
                max_new_tokens=max_new_tokens,
                pad_token_id=self.tokenizer.pad_token_id
            )

        decoded = self.tokenizer.decode(output[0], skip_special_tokens=True)
        # ممكن نقطع الـ response فقط من النص الكامل
        if "<|response|>" in decoded:
            return decoded.split("<|response|>")[1].strip()
        return decoded
