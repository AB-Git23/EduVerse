from django.contrib import admin
from .models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "instructor",
        "price",
        "is_published",
        "average_rating",
        "reviews_count",
        "created_at",
    )
    list_filter = ("is_published", "created_at")
    search_fields = ("title", "description", "instructor__user__username")
    readonly_fields = ("average_rating", "reviews_count", "created_at")
    fieldsets = (
        ("Basic Information", {
            "fields": ("title", "description", "instructor", "price")
        }),
        ("Status", {
            "fields": ("is_published",)
        }),
        ("Statistics", {
            "fields": ("average_rating", "reviews_count")
        }),
        ("Timestamps", {
            "fields": ("created_at",)
        }),
    )
