from django.db import models
from users.models import User
from courses.models import Course


class Review(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not (1 <= self.rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.course.title} ({self.rating}/5)"
