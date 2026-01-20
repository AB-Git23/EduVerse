from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User, VerificationSubmission


@receiver(post_save, sender=User)
def notify_admin_on_instructor_signup(sender, instance, created, **kwargs):
    if created and instance.role == User.ROLE_INSTRUCTOR:
        admin_emails = [email for _, email in getattr(settings, "ADMINS", [])]
        if admin_emails:
            subject = "New instructor signup"
            message = f"New instructor registered: {instance.email} (id: {instance.pk})"
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    admin_emails,
                    fail_silently=False,
                )
            except Exception:
                pass


@receiver(post_save, sender=VerificationSubmission)
def notify_admin_on_submission(sender, instance, created, **kwargs):
    if not created:
        return

    admin_emails = [email for _, email in getattr(settings, "ADMINS", [])]
    if not admin_emails:
        return

    subject = "New instructor verification submission"
    message = (
        f"Instructor {instance.profile.user.email} "
        f"submitted verification documents.\n\n"
        f"Submission ID: {instance.id}"
    )

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, admin_emails)
    except Exception:
        pass


@receiver(post_save, sender=VerificationSubmission)
def notify_instructor_on_review(sender, instance, created, **kwargs):
    if created:
        return

    previous_status = getattr(instance, "_previous_status", None)

    if previous_status == instance.status:
        return  # no state change

    user = instance.profile.user

    if instance.status == VerificationSubmission.STATUS_APPROVED:
        subject = "Your instructor account has been approved"
        message = (
            f"Hi {user.username or user.email},\n\n"
            "Your instructor verification has been approved."
        )

    elif instance.status == VerificationSubmission.STATUS_REJECTED:
        subject = "Your instructor verification was rejected"
        message = (
            f"Hi {user.username or user.email},\n\n"
            "Your verification was rejected.\n\n"
            f"Reason: {instance.rejection_reason}\n\n"
            "Please re-submit your documents."
        )
    else:
        return

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=True,
    )


@receiver(pre_save, sender=VerificationSubmission)
def cache_previous_status(sender, instance, **kwargs):
    if not instance.pk:
        instance._previous_status = None
        return

    try:
        instance._previous_status = (
            VerificationSubmission.objects.only("status").get(pk=instance.pk).status
        )
    except VerificationSubmission.DoesNotExist:
        instance._previous_status = None
