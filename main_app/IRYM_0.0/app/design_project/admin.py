from django.contrib import admin
from .models import DesignProject, DesignPrompt, GeneratedImage

@admin.register(DesignProject)
class DesignProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title", "description")

@admin.register(DesignPrompt)
class DesignPromptAdmin(admin.ModelAdmin):
    list_display = ("project", "prompt_text", "created_at")
    search_fields = ("prompt_text",)

@admin.register(GeneratedImage)
class GeneratedImageAdmin(admin.ModelAdmin):
    list_display = ("prompt", "version", "created_at")
    search_fields = ("prompt__prompt_text",)
