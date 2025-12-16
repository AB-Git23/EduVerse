from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User, InstructorProfile, InstructorVerificationDocument


@receiver(post_save, sender=User)
def notify_admin_on_instructor_signup(sender, instance, created, **kwargs):
    if created and instance.role == User.ROLE_INSTRUCTOR:
        admin_emails = [email for _, email in getattr(settings, 'ADMINS', [])]
        if admin_emails:
            subject = 'New instructor signup'
            message = f'New instructor registered: {instance.email} (id: {instance.pk})'
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, admin_emails, fail_silently=False)
            except Exception:
                pass


@receiver(post_save, sender=InstructorProfile)
def notify_admin_on_profile_created_with_document(sender, instance, created, **kwargs):
    """
    If a profile is created and a verification document is present,
    notify admins (covers case where profile created/updated after initial user).
    """
    if created and instance.verification_document:
        admin_emails = [email for _, email in getattr(settings, 'ADMINS', [])]
        if admin_emails:
            subject = 'Instructor submitted verification documents'
            message = f'Instructor {instance.user.email} (id: {instance.user_id}) uploaded verification documents.'
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, admin_emails, fail_silently=False)
            except Exception:
                pass


@receiver(post_save, sender=InstructorVerificationDocument)
def notify_admin_on_document_upload(sender, instance, created, **kwargs):
    """
    Notify admins whenever an instructor uploads a new verification document.
    """
    if not created:
        return

    admin_emails = [email for _, email in getattr(settings, 'ADMINS', [])]
    if not admin_emails:
        return

    subj = 'Instructor verification document uploaded'
    msg = f"Instructor {instance.profile.user.email} uploaded a verification document (id={instance.id})."
    try:
        send_mail(subj, msg, settings.DEFAULT_FROM_EMAIL, admin_emails, fail_silently=False)
    except Exception:
        # dev: console backend prints; in prod you may want to log exceptions
        pass



@receiver(post_save, sender=InstructorProfile)
def notify_instructor_on_review(sender, instance, created, **kwargs):
    # Do nothing on initial creation (handled above)
    if created:
        return

    # Approved
    if instance.is_verified and not instance.verification_rejected_reason:
        subject = "Your instructor account has been approved"
        message = (
            f"Hi {instance.user.username or instance.user.email},\n\n"
            "Your instructor account has been approved. You can now create and publish courses."
        )
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.user.email], fail_silently=False)
        except Exception:
            pass

    # Rejected
    if instance.verification_rejected_reason:
        subject = "Your instructor verification was rejected"
        message = (
            f"Hi {instance.user.username or instance.user.email},\n\n"
            f"Your verification request was rejected.\n\nReason: {instance.verification_rejected_reason}\n\n"
            "Please update your documents and re-submit."
        )
        try:
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.user.email], fail_silently=False)
        except Exception:
            pass
