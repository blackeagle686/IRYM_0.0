from django.urls import path 
from . import views

urlpatterns = [
    path("design/<int:design_id>/", views.design_view, name="design_view"),
    path("new_design/", views.new_design, name="new_design"),
    path("edit_with_ai/<int:image_id>/", views.edit_with_ai, name="fast_edit_with_ai"),
    path("custom_edit/<int:image_id>/", views.custom_edit, name="custom_edit"),
    path("fast_history/", views.history, name="fast_history")
]

