from django.db import models
from django.contrib.auth.models import User 

# Create your models here.

class FastDesign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.TimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} create Fast Design: {self.title()}"

class DesignPrompts(models.Model):
    fast_design = models.ForeignKey(FastDesign, on_delete=models.CASCADE, related_name="prompts")
    prompt = models.CharField(max_length=500)
    created_at = models.TimeField(auto_now_add=True)
    
    def __str__(self):
        return f"from FastDesign: {self.fast_design.title} this is the prompt {self.prompt[:20]} ...."

class FastGenratedImage(models.Model):
    prompt = models.ForeignKey(DesignPrompts, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='generated/')
    created_at = models.DateTimeField(auto_now_add=True)

class EditFastGenratedImage(models.Model):
    prompt = models.CharField(max_length=500)
    image = models.ImageField(upload_to='generated/')
    created_at = models.DateTimeField(auto_now_add=True)

