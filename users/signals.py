# users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User, InstructorProfile

# 1) Notify admins when a NEW instructor user is created
@receiver(post_save, sender=User)
def notify_admin_on_instructor_signup(sender, instance, created, **kwargs):
    if created and instance.role == User.ROLE_INSTRUCTOR:
        admin_emails = [email for _, email in getattr(settings, 'ADMINS', [])]
        if admin_emails:
            subject = 'New instructor signup'
            message = f'New instructor registered: {instance.email}'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, admin_emails, fail_silently=False)


# 2) Notify instructor when their profile is approved or rejected
@receiver(post_save, sender=InstructorProfile)
def notify_instructor_on_review(sender, instance, created, **kwargs):
    if created:
        return  # do nothing on initial profile creation

    # APPROVED
    if instance.is_verified and not instance.verification_rejected_reason:
        subject = "Your instructor account has been approved"
        message = (
            f"Hi {instance.user.username or instance.user.email},\n\n"
            "Your instructor account has been approved."
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.user.email], fail_silently=False)

    # REJECTED
    if instance.verification_rejected_reason:
        subject = "Your instructor verification was rejected"
        message = (
            f"Hi {instance.user.username or instance.user.email},\n\n"
            f"Your verification request was rejected.\n"
            f"Reason: {instance.verification_rejected_reason}\n\n"
            "Please update your documents and re-submit."
        )
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.user.email], fail_silently=False)
