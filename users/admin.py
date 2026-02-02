from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User,
    StudentProfile,
    InstructorProfile,
    VerificationSubmission,
    InstructorVerificationDocument,
    VerificationAuditLog,
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "username", "role", "is_staff",
                    "is_superuser", "date_joined")
    list_filter = ("role", "is_staff", "is_superuser", "date_joined")
    search_fields = ("email", "username")
    ordering = ("-date_joined",)

    fieldsets = (
        ("Account Information", {
            "fields": ("email", "username", "password")
        }),
        ("Personal Info", {
            "fields": ("first_name", "last_name")
        }),
        ("Role & Permissions", {
            "fields": ("role", "is_staff", "is_superuser", "is_active")
        }),
        ("Timestamps", {
            "fields": ("date_joined", "last_login"),
            "classes": ("collapse",)
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "role")
        }),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("get_email", "get_username", "batch", "enrollment_date")
    list_filter = ("enrollment_date", "batch")
    search_fields = ("user__email", "user__username", "batch")
    readonly_fields = ("enrollment_date",)

    fieldsets = (
        ("User Information", {
            "fields": ("user",)
        }),
        ("Student Details", {
            "fields": ("batch", "enrollment_date")
        }),
    )

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = "Username"


@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ("get_email", "get_username", "expertise", "is_verified")
    list_filter = ("is_verified", "verification_requested_at")
    search_fields = ("user__email", "user__username", "expertise", "bio")
    readonly_fields = ("verification_requested_at",)

    fieldsets = (
        ("User Information", {
            "fields": ("user",)
        }),
        ("Profile Information", {
            "fields": ("bio", "expertise")
        }),
        ("Verification Status", {
            "fields": ("is_verified", "verification_requested_at")
        }),
    )

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = "Username"


@admin.register(VerificationSubmission)
class VerificationSubmissionAdmin(admin.ModelAdmin):
    list_display = ("get_instructor_email", "status",
                    "created_at", "reviewed_at")
    list_filter = ("status", "created_at", "reviewed_at")
    search_fields = ("profile__user__email", "profile__user__username")
    readonly_fields = ("created_at", "reviewed_at")

    fieldsets = (
        ("Instructor", {
            "fields": ("profile",)
        }),
        ("Status", {
            "fields": ("status", "rejection_reason")
        }),
        ("Timestamps", {
            "fields": ("created_at", "reviewed_at")
        }),
    )

    def get_instructor_email(self, obj):
        return obj.profile.user.email
    get_instructor_email.short_description = "Instructor Email"


@admin.register(InstructorVerificationDocument)
class InstructorVerificationDocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "get_instructor_email",
                    "get_submission_status", "uploaded_at")
    list_filter = ("uploaded_at", "submission__status")
    search_fields = ("submission__profile__user__email",)
    readonly_fields = ("uploaded_at",)

    fieldsets = (
        ("Document", {
            "fields": ("submission", "document")
        }),
        ("Timestamps", {
            "fields": ("uploaded_at",)
        }),
    )

    def get_instructor_email(self, obj):
        return obj.submission.profile.user.email
    get_instructor_email.short_description = "Instructor Email"

    def get_submission_status(self, obj):
        return obj.submission.status
    get_submission_status.short_description = "Submission Status"


@admin.register(VerificationAuditLog)
class VerificationAuditLogAdmin(admin.ModelAdmin):
    list_display = ("id", "get_instructor_email", "action", "created_at")
    list_filter = ("action", "created_at")
    search_fields = ("submission__profile__user__email", "notes")
    readonly_fields = ("created_at",)

    fieldsets = (
        ("Submission", {
            "fields": ("submission",)
        }),
        ("Action", {
            "fields": ("action", "notes")
        }),
        ("Timestamps", {
            "fields": ("created_at",)
        }),
    )

    def get_instructor_email(self, obj):
        return obj.submission.profile.user.email
    get_instructor_email.short_description = "Instructor Email"
