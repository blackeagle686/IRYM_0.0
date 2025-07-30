from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>/", views.user_page, name="user_page"),
    path("about/", views.about, name="about"),
    path("api/<int:id>/", views.UserDetailAPIView.as_view(), name="user_detail_api"), #API
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("register/", views.register_user, name="register_user"), # API
    path("login_api/", views.login_user, name="login_user"),   # API endpoint
    path('logout/', views.logout_view, name='logout'),
    path("user_logs_api/", views.users_logs, name="user_logs"), #API
    path("settings/<int:user_id>/", views.user_setttings, name="settings"),
]