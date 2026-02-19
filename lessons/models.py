from django.db import models
from courses.models import Course, Section
from users.models import User


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons_legacy", null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="lessons", null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    content = models.TextField(blank=True, help_text="Markdown content")
    
    # Media
    video_url = models.URLField(blank=True, null=True, help_text="YouTube/Vimeo URL")
    video_file = models.FileField(upload_to="lessons/videos/", blank=True, null=True)
    duration = models.DurationField(blank=True, null=True, help_text="Duration of the lesson")
    
    order = models.PositiveIntegerField()
    is_published = models.BooleanField(default=False)
    is_preview = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order"]
        unique_together = ("section", "order")

    def __str__(self):
        return f"{self.order}. {self.title}"


class LessonResource(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="resources")
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="lessons/resources/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class LessonProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lesson_progress")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="progress")
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "lesson")

    def __str__(self):
        return f"{self.user.email} - {self.lesson.title}"
