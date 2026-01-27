from django.db import models
from users.models import InstructorProfile


class Course(models.Model):
    instructor = models.ForeignKey(
        InstructorProfile, on_delete=models.CASCADE, related_name="courses"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    is_published = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    average_rating = models.FloatField(default=0)
    reviews_count = models.PositiveIntegerField(default=0)


    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

