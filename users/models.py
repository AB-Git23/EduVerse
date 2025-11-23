from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_STUDENT = 'student'
    ROLE_INSTRUCTOR = 'instructor'

    ROLE_CHOICES = (
        (ROLE_STUDENT, 'Student'),
        (ROLE_INSTRUCTOR, 'Instructor'),
    )

    username = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_STUDENT)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

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

