from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_STUDENT = 'student'
    ROLE_INSTRUCTOR = 'instructor'

    ROLE_CHOICES = (
        (ROLE_STUDENT, 'Student'),
        (ROLE_INSTRUCTOR, 'Instructor'),
    )

    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='student')
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.role})"


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='student_profile')
    # enrolled_courses = models.ManyToManyField('courses.Course', blank=True)
    enrollment_date = models.DateField(auto_now_add=True)
    batch = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Student Profile: {self.user.email}"


class InstructorProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='instructor_profile')
    bio = models.TextField(blank=True, null=True)
    expertise = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Instructor Profile: {self.user.email}"

