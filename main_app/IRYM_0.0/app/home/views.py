import os
import uuid
import json
import requests

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import base64
from tasks import generate_description_task  as recommender 

from .models import Logging, Chat, Generation_image, Edited_image
from . import serializers
from . import forms

from design_project.models import GeneratedImage

from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status, filters 

from PIL import Image
from io import BytesIO

templates = settings.TEMPLATES_PATHS

# this is the first version for my project 
ngrok_key = settings.NGROK_KEY
FASTAPI_ENDPOINT_txt2txt = f"{ngrok_key}/generate_image/"
FASTAPI_ENDPOINT_img2img = f"{ngrok_key}/edit_image/"


@require_POST
@csrf_exempt
def generate_recommendation(request):
    prompt = request.POST.get("prompt")

    if not prompt:
        return JsonResponse({"error": "No prompt provided"}, status=400)

    try:
        # تشغيل الموديل
        responses = recommender(prompt)
        response_text = responses[0] if isinstance(responses, list) and responses else responses

        # التأكد من المستخدم
        if not request.user.is_authenticated:
            return JsonResponse({"error": "User not authenticated"}, status=403)


        chat = Chat.objects.filter(user=request.user).last()

        # تسجيل السجل
        Logging.objects.create(
            user=request.user,
            chat=chat,
            prompt=prompt,
            response=response_text,
            log_notes="None"
        )

        return JsonResponse({
            "response": response_text,
            "chat": {
                "id": chat.id,
            }
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)

    
    
@login_required
def logs_view(request):
    if request.user.is_staff: 
        logs = Logging.objects.all().order_by("-timestamp")
        logs_temp = templates['admin'].get("fast_design_logs")
        return render(request, logs_temp, {"logs": logs, "title": "Logs"})
    else:
        return redirect("login") 
    

def hello(request):
    return render(request, templates["hello"], context={'title':"IRYM 0"})



def edit_image(image_path, prompt, save_dir="media/edited"):
    try:
        # اقرأ الصورة وشفّرها إلى base64
        with open(image_path, "rb") as f:
            image_data = f.read()
            image_base64 = base64.b64encode(image_data).decode("utf-8")

        # أرسل الطلب إلى FastAPI
        r = requests.post(
            f"{ngrok_key}/edit_image",
            json={
                "prompt": prompt,
                "image_base64": image_base64
            },
            timeout=120
        )

        if r.status_code != 200:
            return JsonResponse({"error": f"FastAPI error: {r.text}"}, status=500)

        result = r.json()
        if "image_base64" not in result:
            return JsonResponse({"error": "No image returned from FastAPI"}, status=500)

        # فك التشفير وحفظ الصورة
        edited_image_data = base64.b64decode(result["image_base64"])
        filename = f"edited_{uuid.uuid4().hex}.png"
        save_path = os.path.join(settings.MEDIA_ROOT, "edited", filename)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "wb") as f:
            f.write(edited_image_data)

        django_media_url = f"/media/edited/{filename}"

        return {
            "url": django_media_url,
            "success": True
        }

    except Exception as e:
        print("Error:", str(e))
        return JsonResponse({"error": str(e)}, status=500)
    
def edit_with_ai(request):
    if request.method == "POST":
        form = forms.EditWithAIForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data["image"]
            prompt = form.cleaned_data["prompt"]
            
            # ✅ مسار نسبي داخل MEDIA_ROOT
            filename = f"{uuid.uuid4().hex}_{image.name}"
            relative_path = os.path.join("tmp", filename)
            full_path = os.path.join(settings.MEDIA_ROOT, relative_path)

            # ✅ تأكد من وجود المجلد
            os.makedirs(os.path.dirname(full_path), exist_ok=True)

            # ✅ حفظ الملف في media/tmp/
            with open(full_path, "wb+") as temp_file:
                for chunk in image.chunks():
                    temp_file.write(chunk)

            try:
                # ✅ استدعاء API وتمرير المسار الكامل
                response_data = edit_image(full_path, prompt)
                edited_image_url = response_data.get('url', None)  # يجب أن يكون رابط مباشر
                edited_image = Edited_image.objects.create(
                            user=request.user,
                            image=edited_image_url,
                            prompt=prompt.strip()
                        )

            except Exception as e:
                edited_image_url = None
                print(f"API error: {e}")

            # ✅ رابط الصورة الأصلية لعرضها في HTML
            old_image_url = settings.MEDIA_URL + relative_path  # /media/tmp/xxx.png
            edit_with_ai_temp = templates["edit"].get("edit_with_ai")
            return render(
                request,
                edit_with_ai_temp,
                {
                    "form": form,
                    "old_image": old_image_url,
                    "edited_image": edited_image_url,
                    "title": "AI Editor",
                    
                }
            )

    else:
        form = forms.EditWithAIForm()

    return render(request, templates["edit"].get("edit_with_ai"), {"form": form, "title":"AI Editor"})