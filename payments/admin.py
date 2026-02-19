from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "amount", "status", "provider", "created_at")
    list_filter = ("status", "provider", "created_at")
    search_fields = ("user__email", "course__title", "transaction_id")
    readonly_fields = ("created_at", "updated_at")
