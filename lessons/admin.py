from django.contrib import admin
from .models import Lesson, LessonResource, LessonProgress


class LessonResourceInline(admin.TabularInline):
    model = LessonResource
    extra = 1


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "section", "order", "is_published", "is_preview", "duration", "created_at")
    list_filter = ("is_published", "is_preview", "section__course")
    search_fields = ("title", "description", "section__title", "section__course__title")
    readonly_fields = ("created_at", "updated_at")
    inlines = [LessonResourceInline]
    ordering = ("section__course", "section__order", "order")


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "lesson", "is_completed", "completed_at")
    list_filter = ("is_completed", "completed_at")
    search_fields = ("user__email", "lesson__title")
    readonly_fields = ("completed_at", "updated_at")
