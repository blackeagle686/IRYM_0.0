from django.db import models
from django.contrib.auth.models import User
        
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
    message = models.TextField(default="Hello", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Chat by {self.user.username} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "message": self.message,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        }    
    
    
    
class Generation_image(models.Model):
    image = models.ImageField(upload_to='generated/', blank=True, null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='generated_images')
    
    def __str__(self):
        return f"Image from Chat {self.chat.id}"

class Logging(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, null=True, blank=True)
    prompt = models.CharField(max_length=400)
    response = models.CharField(max_length=400)
    log_notes = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-timestamp']
        
class Edited_image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='edited/')
    prompt = models.CharField(max_length=800)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-timestamp']
    def __str__(self):
        return f"Image from Chat {self.chat.id}"