from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.html import format_html
from .models import User, StudentProfile, InstructorProfile, InstructorVerificationDocument

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    list_display = ('email', 'username', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_staff', 'is_superuser'),
        }),
    )

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'enrollment_date', 'batch')
    

class InstructorVerificationDocumentInline(admin.TabularInline):
    model = InstructorVerificationDocument
    extra = 0
    readonly_fields = ('filename', 'document', 'uploaded_at')
    can_delete = True


@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_verified', 'verification_requested_at', 'doc_link', 'verification_rejected_reason')
    readonly_fields = ('verification_document',)
    inlines = [InstructorVerificationDocumentInline]

    def doc_link(self, obj):
        if obj.verification_document:
            return format_html('<a href="{}" target="_blank">document</a>', obj.verification_document.url)
        return "-"
    doc_link.short_description = 'Document'




