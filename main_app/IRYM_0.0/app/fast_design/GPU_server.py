from django.conf import settings

import requests
import os 
import uuid 

from io import BytesIO
import base64
from django.core.files.base import ContentFile

from .models import FastGenratedImage, DesignPrompts, EditFastGenratedImage
from design_project.models import DesignPrompt, GeneratedImage

GPU_SERVER_URL = settings.NGROK_KEY 
GPU_GENERATE = f"{GPU_SERVER_URL}/generate_image"
GPU_EDIT = f"{GPU_SERVER_URL}/edit_image"

def handle_image(image_bytes, design=None, prompt_txt=None, prompt_obj_txt=None, edit=False):
    # فك الصورة من base64
    try:
        image_data = base64.b64decode(image_bytes)
    except Exception as e:
        print(f"[ERROR] Failed to decode image bytes: {e}")
        return None

    image_name = f"{uuid.uuid4()}.png"
    image_file = ContentFile(image_data, name=image_name)

    try:
        if edit:
            # إذا تعديل، نحاول حفظها تحت GeneratedImage المرتبط بـ DesignPrompt
            try:
                prompt = DesignPrompt.objects.create(prompt=prompt_txt)
                image = GeneratedImage.objects.create(prompt=prompt, image=image_file)
            except Exception as e:
                print(f"[WARN] Could not create DesignPrompt or GeneratedImage, saving as EditFastGenratedImage: {e}")
                image = EditFastGenratedImage.objects.create(prompt=prompt_txt, image=image_file)
        else:
            # إذا إنشاء جديد، نحفظ باستخدام FastGenratedImage
            prompt_obj = DesignPrompts.objects.create(fast_design=design, prompt=prompt_obj_txt)
            image = FastGenratedImage.objects.create(prompt=prompt_obj, image=image_file)

        image.save()
        return image

    except Exception as e:
        print(f"[ERROR] Failed to save image object: {e}")
        return None


def generate_image_fast_design(prompt, design): 
    try:
        response = requests.post(
            GPU_GENERATE, 
            json={"text": prompt},
            timeout=60
        )
        
        if response.status_code == 200:
            generated_image = response.json().get("image_base6")
            return handle_image(generated_image, design, prompt_obj_txt=prompt)
        else:
            print("Error:", response.status_code, response.text)
            return None

    except Exception as e:
        print("Error during image generation:", str(e))
        return None 


def edit_fast_design_generated_image(image_base64, prompt):
    try:
        response = requests.post(
            GPU_EDIT,
            json={
                "prompt": prompt,
                "image_base64": image_base64 
            },
            timeout=60
        )

        if response.status_code == 200:
            result_json = response.json()
            edited_base64 = result_json.get("image_base64")

            if not edited_base64:
                print("No image returned.")
                return None
            
            return handle_image(edited_base64, prompt_txt=prompt, edit=True)

        else:
            print("Error:", response.status_code, response.text)
            return None
        
    except Exception as e:
        print("Error during image editing:", str(e))
        return None
