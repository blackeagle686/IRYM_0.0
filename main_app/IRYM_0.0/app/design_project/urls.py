from django.urls import path
from . import views 

urlpatterns = [
    path("new_project/", views.new_project, name="new_project"),
    path("design/<int:project_id>/", views.project_view, name="project_view"),
    path("edit_room/<int:image_id>/", views.edit_room, name="edit_room"), 
    path("projects_history/", views.projects_history, name="projects_history"),
    path('project_detail/<int:project_id>/', views.project_detail, name='project_detail'),
    path('edit_with_ai/<int:image_id>/', views.edit_project_with_ai, name='edit_project_with_ai'),
    path('project/<int:pk>/update/', views.update_project, name='update_project'),

]
