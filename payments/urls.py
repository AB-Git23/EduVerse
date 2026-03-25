from django.urls import path
from .views import CreateCheckoutSessionView, StripeWebhookView

urlpatterns = [
    path(
        "create-checkout-session/<int:course_id>/",
        CreateCheckoutSessionView.as_view(),
        name="create-checkout-session",
    ),
    path(
        "webhook/",
        StripeWebhookView.as_view(),
        name="stripe-webhook",
    ),
]
