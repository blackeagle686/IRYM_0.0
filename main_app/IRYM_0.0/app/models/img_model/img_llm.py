# main_app/image_generator.py

import torch
from diffusers import StableDiffusionPipeline
from PIL import Image
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_saved = os.path.join(BASE_DIR, "my_sd_model")
cash_model = "runwayml/stable-diffusion-v1-5"

# نختار المسار المحلي إذا موجود، وإلا نحمل من الإنترنت
model_path = model_saved if os.path.exists(model_saved) else cash_model

# مسار الصورة الناتجة (ملف صورة)
IMG_path = os.path.join(BASE_DIR, "generated_imgs_test", "generated_image.png")

class ImageGenerator:
    def __init__(self, model_name=model_path, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.pipe = StableDiffusionPipeline.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
        ).to(self.device)

    def generate(self, prompt, output_path=IMG_path):
        # تأكد أن المجلد موجود
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # توليد الصورة
        result = self.pipe(prompt)
        image = result.images[0]
        image.save(output_path)
        return image

# حمّل النموذج مرة واحدة
img_generator = ImageGenerator()

# pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5")
# pipe.save_pretrained("./my_sd_model")  # يحفظ نسخة محليًا

# prompt = "A beautiful sunset over the ocean"
# img_generator.generate(prompt)