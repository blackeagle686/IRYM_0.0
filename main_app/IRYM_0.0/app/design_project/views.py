from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.files.base import ContentFile
from .forms import EditImageForm

from fast_design import GPU_server
from fast_design.forms import EditForm

from .forms import DesignProjectForm
from .models import *

import uuid
import requests
import os
import base64

from PIL import Image
import io
import requests as reqs

# Create your views here.

templates = settings.TEMPLATES_PATHS

ng_key = settings.NGROK_KEY

def generate_multi_images(prompt):
    # send the prmopt to the model on FastAPI endpint on GpuRuntime using googleColab
    response = requests.post(f"{ng_key}/multi_image_generation", json={"text": prompt}, timeout=90)
    
    #check if response is successful
    if response.status_code != 200:
        return JsonResponse({"error": "Image generation failed"}, status=500)
    
    # get the images that were generated 
    data = response.json() 
    
    # check if the data is empty
    if "urls" not in data:
        return JsonResponse({"error": "Image URL not returned from FastAPI"}, status=500)
    
    # the final results use this in Project_view function
    images = data["urls"]
    return images



def edit_uploaded_image(image_bytes, prompt):
    try:
        
        image_tuple = ('image.png', image_bytes, 'image/png')
        
        response = requests.post(
            f"{ng_key}/edit_image",
            files={'image': image_tuple},
            data={'prompt': prompt},
            timeout=60
        )

        if response.status_code == 200:
            # استلام الصورة المعدلة كـ bytes
            result = response.content

            # توليد اسم فريد للملف
            filename = f"{uuid.uuid4().hex}.png"
            edited_dir = os.path.join(settings.MEDIA_ROOT, "edited")
            os.makedirs(edited_dir, exist_ok=True)
            file_path = os.path.join(edited_dir, filename)

            # حفظ الصورة
            with open(file_path, 'wb') as f:
                f.write(result)

            # إرجاع المسار النسبي
            return f"/media/edited/{filename}"

        else:
            print("Error:", response.status_code, response.text)
            return None

    except Exception as e:
        print("Error during image editing:", str(e))
        return None

def is_server_ready():
    try: 
        response = requests.get(f"{ng_key}/is_available", timeout=10)
        data = response.json() 
        return data.get('ready', False) 
    except requests.exceptions.RequestException:
        return False


@login_required
def project_view(request, project_id):
    project = get_object_or_404(DesignProject, id=project_id)
    images = []
    
    if request.method == "POST":
        prompt_text = request.POST.get("prompt")
        print(prompt_text)
        if prompt_text:
            # 1. Create Prompt
            prompt = DesignPrompt.objects.create(project=project, prompt_text=prompt_text)

            # 2. Generate images from FastAPI
            image_urls = generate_multi_images(prompt_text)

            # 3. Save images to DB
            for idx, url in enumerate(image_urls):
                try:
                    full_url = f"{ng_key}/{url}"  # أو حط المسار كامل حسب نظامك
                    response = requests.get(full_url)
                    if response.status_code == 200:
                        image_content = ContentFile(response.content)
                        GeneratedImage.objects.create(
                        prompt=prompt,
                        image=ContentFile(response.content, name=f"generated_{uuid.uuid4().hex}.png"),
                        version=idx + 1
                        )

                except Exception as e:
                    print(f"Error saving image: {e}")

            # نحدث الصور المعروضة
            images = prompt.images.all()

    else:
        # لو GET، نعرض آخر prompt وصوره
        last_prompt = project.prompts.last()
        if last_prompt:
            images = last_prompt.images.all()
    template = templates["generate"].get("project")
    return render(request, template, {
        "project": project,
        "title": f"{project.title}",
        "images": images,
        "is_server_work":is_server_ready(),
        
    })
    
    
@login_required
def new_project(request):
    if request.method == 'POST':
        form = DesignProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.save()
            return redirect('project_view', project_id=project.id) 
    else:
        form = DesignProjectForm()
    
    return render(request, templates['forms'].get("new_project"), {'form': form, "title":"New Design Project"})


@login_required
def edit_room(request, image_id):
    image = get_object_or_404(GeneratedImage, id =image_id)
    image = image.image.url 
    print(image)
    return render(request, templates["edit"].get("edit_room"), {'image': image, 'title': "Edit Room"})


@login_required
def projects_history(request):
    projects = DesignProject.objects.filter(user=request.user).order_by('-created_at')
    for project in projects:
        print(project.title)
    return render(request, templates["history"].get("project_history"), {'projects': projects, "title": "Projects History"})


@login_required
def project_detail(request, project_id):
    project = get_object_or_404(DesignProject, id=project_id)
    prompts = project.prompts.all()
    
    data = [
        {
            "prompt": prompt,
            "images": [image for image in prompt.images.all()]
        }
        for prompt in prompts
    ]
    print(data)
    
    return render(request, templates["details"].get("project_details"), {
        "project": project,
        "title": f"{project.title}",
        "data": data,
    })






@login_required
def edit_project_with_ai(request, image_id):
    image_obj = get_object_or_404(GeneratedImage, id=image_id)
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
def update_project(request, pk):
    project = get_object_or_404(DesignProject, id=pk)

    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.goal = request.POST.get('goal')
        project.description = request.POST.get('description')
        project.status = request.POST.get('status')
        project.save()

    return redirect('project_detail', project_id=project.id)