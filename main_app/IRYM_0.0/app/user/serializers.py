from django.contrib.auth.models import User
from rest_framework import serializers
from . import models 

class User_serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']                
        
class UserProfile_serializer(serializers.ModelSerializer):
    class Meta: 
        model = models.UserProfile 
        fields= ["user_image", ]
        
        
class UserLogs_serializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

    class Meta:
        model = models.UserLogs
        fields = ['id', 'username', 'op_type', 'timestamp']  # أو "__all__" لو عايز كل حاجة

    def get_username(self, obj):
        return obj.user.username if obj.user else "Anonymous"
