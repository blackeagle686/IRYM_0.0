# main_app/image_generator.py

import torch
from diffusers import StableDiffusionPipeline
from PIL import Image

class ImageGenerator:
    def __init__(self, model_name="runwayml/stable-diffusion-v1-5", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        )
        self.pipe = self.pipe.to(self.device)

    def generate(self, prompt, output_path="generated_image.png"):
        result = self.pipe(prompt)
        image = result.images[0]
        image.save(output_path)
        return image
