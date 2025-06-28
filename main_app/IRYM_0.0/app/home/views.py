from django.shortcuts import render
from genertion import *
# Create your views here.

import requests
from django.http import JsonResponse


def generate_image(request):
    if request.method == "POST":
        prompt = request.POST.get("prompt", "")
        response = requests.post(
            "http://127.0.0.1:5000",  # اللينك اللي طلع من Colab
            json={"prompt": prompt}
        )
        if response.status_code == 200:
            image_base64 = response.json()["image_base64"]
            return JsonResponse({"image": image_base64})
        else:
            return JsonResponse({"error": "Something went wrong"}, status=500)
