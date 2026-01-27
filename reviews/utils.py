from django.db.models import Avg
from .models import Review


def update_course_rating(course):
    qs = Review.objects.filter(course=course)

    course.average_rating = qs.aggregate(
        avg=Avg("rating")
    )["avg"] or 0

    course.reviews_count = qs.count()
    course.save()
