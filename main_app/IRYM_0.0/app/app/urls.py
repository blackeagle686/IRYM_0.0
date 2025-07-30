from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),                         # Admin
    path('user/', include('user.urls')),                    # Home
    path('project/', include('design_project.urls')),       # User
    path('fast_design/', include('fast_design.urls')),      # Fast Design
    
]

# handling the media urls
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
