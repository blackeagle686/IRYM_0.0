from django.urls import path
from . import views

urlpatterns = [
    path("", views.hello, name="hello"),
    path("logs/", views.logs_view, name='logs'), 
    path("edit_with_ai_upload_image/", views.edit_with_ai, name="edit_with_ai_upload_image"),
]
