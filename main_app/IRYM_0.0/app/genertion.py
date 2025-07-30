# main_app/generation.py

from models.img_model.img_llm import ImageGenerator, img_generator, IMG_path
from models.text_llm.text_llm_responder import LLMResponder, responder
def generate_recommendation(user_prompt: str) -> str:
    llm = responder
    generated_description = llm.generate_response(user_prompt)
    print(f"Generated Description: {generated_description}")
    return generated_description

def generate_image_from_description(description: str, image_path: str = "output.png"):
    image_generator = img_generator
    image_generator.generate(description, output_path=image_path)
    print(f"Image saved at {image_path}")
    return image_path


# respond1 = generate_recommendation("red tree.")
# img1 = generate_image_from_description(description=respond1, image_path=IMG_path)