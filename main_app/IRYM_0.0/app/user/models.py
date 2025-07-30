from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    user_image = models.ImageField(upload_to='user_images/', default="/user_images/majestic-mountain-peak-tranquil-winter-landscape-generated-by-ai.jpg")
    
    def __str__(self):
        return str(self.user.id)
    
    
    
class UserLogs(models.Model): 
    OPERATION_TYPES = [
        ("login", "Login"),
        ("signup", "Signup"),
        ("logout", "Logout"),
    ]

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    op_type = models.CharField(max_length=10, choices=OPERATION_TYPES, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} - {self.op_type} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"