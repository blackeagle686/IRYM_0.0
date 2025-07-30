from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout , login
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

from home.models import Chat, Generation_image
from home.serializers import Chat_images_serilizer, Chat_serilizer

from .models import UserProfile, UserLogs
from . import serializers 
from .db_query import User_query, Design_query
from design_project.models import DesignProject

from rest_framework.views import APIView
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from rest_framework.permissions import IsAuthenticated

import json
class UserDetailAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        user_profile = get_object_or_404(UserProfile, user=user)

        user_ser = serializers.User_serializer(user)
        user_profile_ser = serializers.UserProfile_serializer(user_profile)

        data = {
            "user": user_ser.data,
            "user_image": user_profile_ser.data
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, id):
        user = get_object_or_404(User, id=id)
        user_profile = get_object_or_404(UserProfile, user=user)

        print("Request data:", request.data)  # Debug

        user_ser = serializers.User_serializer(user, data=request.data, partial=True)
        user_profile_ser = serializers.UserProfile_serializer(user_profile, data=request.data, partial=True)

        if user_ser.is_valid() and user_profile_ser.is_valid():
            user_ser.save()
            user_profile_ser.save()
            return Response({
                "user": user_ser.data,
                "user_image": user_profile_ser.data
            }, status=status.HTTP_200_OK)

        return Response({
            "user_errors": user_ser.errors,
            "user_profile_errors": user_profile_ser.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, id):
        user = get_object_or_404(User, id=id)
        user_profile = get_object_or_404(UserProfile, user=user)

        user_profile.delete()
        user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

templates = settings.TEMPLATES_PATHS

# ------------------------------------------- User Page View -------------------------------------------

@login_required
def user_page(request, id: int):
    # If staff, redirect to logs (admins shouldn't view user pages directly)
    if request.user.is_staff:
        return redirect("logs")

    # If the user is trying to access another user's page, forbid it
    if request.user.id != id:
        return HttpResponseForbidden(" Access denied. You cannot view another user's page.")

    # Fetch user data using query object
    user_query = User_query(id)
    user_data = user_query.get_data()
    projects = DesignProject.objects.filter(user_id=id).order_by("-created_at")[:5]
    # Limit the chats shown
    user_data["chats"] = user_data.get("chats", [])[:5]  
    user_page = templates["user"].get("user_page")  
    return render(
        request,
        user_page,
        {
            "user_data": user_data,
            "title": user_data.get("fullname", "User"),
            "projects": projects,
        }
    )

 
# ------------------------------------------- Account OP ----------------------------------------------

# Account operations Loign, Signup, Logout and them API's
def login_view(request): 
    login_template = templates["forms"].get("login")
    return render(request, login_template)

def signup_view(request): 
    register_temp = templates['forms'].get("signup")
    return render(request, register_temp)

@login_required
def logout_view(request):
    user = request.user 
    logout(request)
    logs = UserLogs.objects.create(user=user, op_type="logout")
    return redirect('login')  

@api_view(["POST"])
def register_user(request):
    username = request.data.get("username")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    password = request.data.get("password")
    password2 = request.data.get("password2")

    if not all([username, first_name, last_name, password, password2]):
        return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

    if password != password2:
        return Response({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password)
    logs = UserLogs.objects.create(user=user, op_type="signup")
    user_image = UserProfile.objects.create(user=user)
    return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
    
@api_view(["POST"])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        logs = UserLogs.objects.create(user=user, op_type="login")
        return Response({"message": "Login successful", "id": user.id}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(["GET"])
def users_logs(request):
    loggings = UserLogs.objects.all().order_by("-timestamp")
    serializer = serializers.UserLogs_serializer(loggings, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

def about(request):
    return render(request, "about.html")

# ------------------------------------------- User settings -------------------------------------------
"""
user settings that user can change his name and image
using View Based Class form the class that called UserDetailAPIView 
"""
@login_required
def user_setttings(request, user_id):
    query = User_query(user_id=user_id)
    user = query.get_data()
    user_settngs_temp = templates["user"].get("user_settings")
    return render(request, user_settngs_temp, {"client": user, "title":"Settings", "user_id":request.user.id})



