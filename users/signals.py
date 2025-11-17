from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, StudentProfile, InstructorProfile

# @receiver(post_save, sender=User)
# def create_role_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.role == User.ROLE_STUDENT:
#             StudentProfile.objects.create(user=instance)
#         elif instance.role == User.ROLE_INSTRUCTOR:
#             InstructorProfile.objects.create(user=instance)


# @receiver(post_save, sender=StudentProfile)
# def set_student_role(sender, instance, created, **kwargs):
#     if created:
#         instance.user.role = User.ROLE_STUDENT
#         instance.user.save()


# @receiver(post_save, sender=InstructorProfile)
# def set_instructor_role(sender, instance, created, **kwargs):
#     if created:
#         instance.user.role = User.ROLE_INSTRUCTOR
#         instance.user.save()
