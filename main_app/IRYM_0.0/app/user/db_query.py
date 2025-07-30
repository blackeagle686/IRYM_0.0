from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib.auth import authenticate, logout , login
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from home.models import Chat, Generation_image
from home.serializers import Chat_serilizer , Chat_images_serilizer
from .models import UserProfile
from . import serializers 

from abc import ABC, abstractmethod

class IQuery(ABC):
    @abstractmethod
    def query(self):
        """Should return a queryset or execute a query."""
        pass 

    @abstractmethod
    def get_data(self):
        """Should return the raw or processed data."""
        pass 

    @abstractmethod
    def get_serializer_data(self):
        """Should return the serializer class for general data."""
        pass 

class User_query(IQuery):
    def __init__(self, user_id):
        self.id = user_id 
        self.__data = {}
        self.__user_serializer = None 
        self.__user_image_serializer = None 
        self.__user = None
        self.query()  
        
    def query(self):
        try:
            user = User.objects.get(id=self.id)        
            self.__user = user
            user_profile = UserProfile.objects.get(user=user)
            user_chats = Chat.objects.filter(user=user).order_by("-timestamp")
            self.__data = {
                "username": user.username,
                "image": user_profile.user_image.url if user_profile.user_image else None,
                "ser": serializers.User_serializer(user).data,
                "fullname": user.get_full_name(),
                "fname": user.first_name,
                "lname": user.last_name,
                "chats": user_chats,
                
            }
            self.__user_serializer = serializers.User_serializer(user)
            self.__user_image_serializer = serializers.UserProfile_serializer(user_profile)
            
        except Exception as e:
            print(f"Error fetching user data: {e}")
    
    def get_user(self):
        return self.__user
    
    def get_data(self):
        return self.__data
    
    def get_serializer_data(self):
        data = {
            "user": self.__user_serializer.data,
            "image": self.__user_image_serializer.data 
        }
        return data
    
    def __str__(self):
        return f"UserI<{self.__data.get('username', 'Unknown')}>"
    
    
class Design_query(IQuery): 
    def __init__(self, design_id):
        self.design_id = design_id 
        self.__design_data = None
        self.__design_serializer = None 
        self.query() 
        
    def query(self):
        try:
            design = Chat.objects.get(id=self.design_id)
            print(f"Chat ID: {design.id}")
            
            design_imgs = Generation_image.objects.filter(chat=design)
            print(f"Design Images: {design_imgs}")
            
            last_img = design_imgs.last()
            print(f"Last Image: {last_img.image.url}")
            
            self.__design_data = {
                "id": self.design_id,
                "user": design.user.username,
                "message": design.message,
                "images": [img.image.url for img in design_imgs if img.image],  
                "last_img": last_img.image.url if last_img and last_img.image else None,
            }

            self.__design_serializer = Chat_serilizer(design)

        except Chat.DoesNotExist:
            print(f"design with id={self.design_id} does not exist.")
        except Exception as e:
            print(f"Error fetching design data: {e}")
    
    def get_data(self):
        return self.__design_data
    
    def get_serializer_data(self):
        return {
            "design": self.__design_serializer.data if self.__design_serializer else {}
        }

    def __str__(self):
        return f"designQuery<{self.__design_data.get('user', 'Unknown')}>"

