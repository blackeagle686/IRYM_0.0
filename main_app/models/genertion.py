# main_app/generation.py

from img_llm.img_llm import ImageGenerator 
from text_llm.text_llm_responder import LLMResponder

def generate_recommendation(user_prompt: str) -> str:
    llm = LLMResponder()
    generated_description = llm.generate_response(user_prompt)
    print(f"🧠 Generated Description: {generated_description}")
    return generated_description

def generate_image_from_description(description: str, image_path: str = "output.png"):
    image_generator = ImageGenerator()
    image_generator.generate(description, output_path=image_path)
    print(f"Image saved at {image_path}")
    return image_path
