from django.db import models
from users.models import User
from courses.models import Course


class Review(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
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


# Signals to update course rating
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg

@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_course_rating(sender, instance, **kwargs):
    course = instance.course
    reviews = course.reviews.all()
    if reviews.exists():
        course.average_rating = reviews.aggregate(Avg("rating"))["rating__avg"]
        course.reviews_count = reviews.count()
    else:
        course.average_rating = 0
        course.reviews_count = 0
    course.save()
