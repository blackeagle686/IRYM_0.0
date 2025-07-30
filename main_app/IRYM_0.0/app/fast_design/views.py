from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import requests 
from django.conf import settings 
from django.contrib import messages
from .models import *
from .forms import FastDesignForm, EditForm
from . import GPU_server

from PIL import Image
import io
import os
import requests as reqs
import base64
# Create your views here.

ng_key = settings.NGROK_KEY
templates = settings.TEMPLATES_PATHS

# ------------------------------------------- Fast Design View -------------------------------------------


@login_required
def design_view(request, design_id): 
    design = get_object_or_404(FastDesign, id=design_id)
    generated_image_url = None  # لتفادي UnboundLocalError
    image_id = None
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        generated_image = GPU_server.generate_image_fast_design(prompt, design)
        generated_image_url=generated_image.image.url
        image_id = generated_image.id 
    return render(request, templates['generate'].get('fast_design_generate'), {
        "design": design,
        "title": f"Design {design_id}",
        "image": generated_image_url,
        "image_id": image_id, 
    })



@login_required
def new_design(request):
    if request.method == 'POST':
        form = FastDesignForm(request.POST)
        if form.is_valid():
            design = form.save(commit=False)
            design.user = request.user
            design.save()
            return redirect('design_view', design_id=design.id)  # غيرها حسب اسم URL عندك
    else:
        form = FastDesignForm()
    return render(request, 'forms/new_fast_design.html', {'form': form, "title":"New Fast Design Project"})



# ------------------------------------------- Editing Fast Design View -------------------------------------------

@login_required
def edit_with_ai(request, image_id):
    image_obj = get_object_or_404(FastGenratedImage, id=image_id)
    image_url = image_obj.image.url  # مثال: /media/generated/abc.png
    edited_image_url = None
    edited_image = None
    
    image_path = image_obj.image.path
    with Image.open(image_path) as img:
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    
    if request.method == 'POST':
        form = EditForm(request.POST)

        if form.is_valid():
            prompt = form.cleaned_data['prompt']
            print(type(prompt))
            edited_image = GPU_server.edit_fast_design_generated_image(image_base64, prompt)
            
            if edited_image:
                edited_image_url = edited_image.image.url

    else:
        form = EditForm()

    return render(request, "pages/edit/edit.html", {
        "title": "Edit with AI",
        "form": form,
        "edited_image_url": edited_image_url,
        "original_image_url": image_url,
        "edited_image": edited_image, 
    })   
    
    
@login_required
def custom_edit(request, image_id):
    image = get_object_or_404(FastGenratedImage, id=image_id)
    image_url = image.url
    return render(request, 'pages/edit/edit_room.html', {'image': image_url, 'title': "Edit Room"})


# ------------------------------------------- User Fast Designs History View -------------------------------------------

@login_required
def history(request):
    fast_designs = FastDesign.objects.filter(user=request.user)
    
    
    return render(request, "pages/history/fast_design_history.html", {
        "title": "History",
        "designs": fast_designs,
    })