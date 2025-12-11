# tasks/admin.py
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "status", "created_at")
    list_filter = ("status", "created_at", "owner")
    search_fields = ("title", "description", "owner__username")
