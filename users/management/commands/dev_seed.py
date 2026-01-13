from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from courses.models import Course
from enrollments.models import Enrollment

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = "Seed full development data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding users...")

        instructors = []
        for _ in range(3):
            user = User.objects.create_user(
                email=fake.email(),
                password="password123",
                is_instructor=True
            )
            instructors.append(user)

        students = []
        for _ in range(10):
            user = User.objects.create_user(
                email=fake.email(),
                password="password123"
            )
            students.append(user)

        self.stdout.write("Seeding courses...")

        courses = []
        for instructor in instructors:
            for _ in range(2):
                course = Course.objects.create(
                    title=fake.sentence(),
                    instructor=instructor
                )
                courses.append(course)

        self.stdout.write("Seeding enrollments...")

        for student in students:
            for course in courses[:3]:
                Enrollment.objects.get_or_create(
                    user=student,
                    course=course
                )

        self.stdout.write(self.style.SUCCESS("Development data ready."))
