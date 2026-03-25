from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("course", "student", "rating", "created_at")
    list_filter = ("rating", "created_at", "course")
    search_fields = ("student__username", "student__email", "course__title", "comment")
    readonly_fields = ("created_at",)
