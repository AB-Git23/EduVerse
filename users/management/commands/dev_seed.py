import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from faker import Faker
from users.models import InstructorProfile, StudentProfile
from courses.models import Course
from enrollments.models import Enrollment
from lessons.models import Lesson

User = get_user_model()
fake = Faker()


class Command(BaseCommand):
    help = "Seeds the database with realistic development data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        with transaction.atomic():
            self.create_superuser()
            instructors = self.create_instructors()
            students = self.create_students()
            courses = self.create_courses(instructors)
            self.create_lessons(courses)
            self.create_enrollments(students, courses)

        self.stdout.write(self.style.SUCCESS("Successfully seeded data."))

    def create_superuser(self):
        email = "admin@eduverse.com"
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(
                email=email, username="admin", password="password123"
            )
            self.stdout.write(f"Created superuser: {email}")
        else:
            self.stdout.write(f"Superuser {email} already exists")

    def create_instructors(self, count=5):
        instructors = []
        for _ in range(count):
            email = fake.unique.email()
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    email=email,
                    username=fake.user_name(),
                    password="password123",
                    role=User.ROLE_INSTRUCTOR,
                )
                InstructorProfile.objects.create(
                    user=user,
                    bio=fake.paragraph(),
                    expertise=fake.job(),
                    is_verified=True,
                    verification_requested_at=fake.date_time_this_year(),
                )
                instructors.append(user)
        self.stdout.write(f"Created {len(instructors)} new instructors")
        # Return all instructors, including existing ones if we didn't create enough new ones (simplified for now)
        return User.objects.filter(role=User.ROLE_INSTRUCTOR)

    def create_students(self, count=20):
        students = []
        for _ in range(count):
            email = fake.unique.email()
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_user(
                    email=email,
                    username=fake.user_name(),
                    password="password123",
                    role=User.ROLE_STUDENT,
                )
                StudentProfile.objects.create(
                    user=user, batch=f"Batch {random.randint(1, 5)}"
                )
                students.append(user)
        self.stdout.write(f"Created {len(students)} new students")
        return User.objects.filter(role=User.ROLE_STUDENT)

    def create_courses(self, instructors, count_per_instructor=3):
        courses = []
        for instructor in instructors:
            # Check if instructor already has courses to avoid over-seeding on re-runs
            if instructor.instructor_profile.courses.count() >= count_per_instructor:
                continue

            for _ in range(count_per_instructor):
                course = Course.objects.create(
                    instructor=instructor.instructor_profile,
                    title=fake.catch_phrase(),
                    description=fake.text(),
                    is_published=True,
                )
                courses.append(course)
        self.stdout.write(f"Created {len(courses)} new courses")
        return Course.objects.all()

    def create_lessons(self, courses):
        lessons_created = 0
        for course in courses:
            # If course already has lessons, skip adding more to ensure idempotency approx
            if course.lessons.exists():
                continue

            num_lessons = random.randint(3, 8)
            for i in range(1, num_lessons + 1):
                Lesson.objects.create(
                    course=course,
                    title=fake.sentence(nb_words=4),
                    content=fake.paragraph(),
                    order=i,
                    is_published=True,
                )
                lessons_created += 1
        self.stdout.write(f"Created {lessons_created} new lessons")

    def create_enrollments(self, students, courses):
        enrollments_created = 0
        if not courses.exists():
            return

        for student in students:
            # Randomly enroll in 1-5 courses
            courses_to_enroll = random.sample(
                list(courses), k=min(len(courses), random.randint(1, 5))
            )
            for course in courses_to_enroll:
                if not Enrollment.objects.filter(
                    student=student, course=course
                ).exists():
                    Enrollment.objects.create(student=student, course=course)
                    enrollments_created += 1
        self.stdout.write(f"Created {enrollments_created} new enrollments")
