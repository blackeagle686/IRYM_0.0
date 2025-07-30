from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DesignProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    goal = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=[
        ("draft", "Draft"),
        ("published", "Published"),
        ("completed", "Completed"),
    ], default="draft")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class DesignPrompt(models.Model):
    project = models.ForeignKey(DesignProject, on_delete=models.CASCADE, related_name="prompts")
    prompt_text = models.TextField()
    style = models.CharField(max_length=100, blank=True)  # Optional: ممكن تحدد ستايل معين
    created_at = models.DateTimeField(auto_now_add=True)

class GeneratedImage(models.Model):
    prompt = models.ForeignKey(DesignPrompt, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="generated/")
    version = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    feedback = models.TextField(blank=True)
