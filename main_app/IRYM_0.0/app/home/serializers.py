from rest_framework import serializers

from . import models 

class Chat_serilizer(serializers.ModelSerializer):
    class Meta:
        model = models.Chat
        fields = '__all__'
        
class Chat_images_serilizer(serializers.ModelSerializer):
    class Meta:
        model = models.Generation_image
        fields = '__all__'
    