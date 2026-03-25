import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from courses.models import Course
from enrollments.models import Enrollment
from .models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        course = get_object_or_404(Course, pk=course_id)

        # Check if already enrolled
        if Enrollment.objects.filter(student=request.user, course=course).exists():
            return Response(
                {"detail": "You are already enrolled in this course."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create Stripe Checkout Session
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                customer_email=request.user.email,
                line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "product_data": {
                                "name": course.title,
                                "description": course.description[:255] if course.description else "Course Enrollment",
                            },
                            "unit_amount": int(course.price * 100),  # Stripe expects cents
                        },
                        "quantity": 1,
                    }
                ],
                mode="payment",
                # Hardcoded URLs for now until frontend is fully hooked up
                success_url="http://localhost:3000/courses/{}/success?session_id={{CHECKOUT_SESSION_ID}}".format(course.id),
                cancel_url="http://localhost:3000/courses/{}/cancel".format(course.id),
                metadata={
                    "course_id": course.id,
                    "user_id": request.user.id,
                },
            )

            # Record pending payment in database
            Payment.objects.create(
                user=request.user,
                course=course,
                amount=course.price,
                status=Payment.STATUS_PENDING,
                provider="stripe",
                transaction_id=checkout_session.id,
            )

            return Response({"checkout_url": checkout_session.url})
        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StripeWebhookView(APIView):
    permission_classes = [AllowAny]  # Webhooks come from Stripe, not authenticated users
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET

        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Handle the event
        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            self.handle_checkout_session_completed(session)

        return Response(status=status.HTTP_200_OK)

    def handle_checkout_session_completed(self, session):
        # Retrieve metadata
        course_id = session.get("metadata", {}).get("course_id")
        user_id = session.get("metadata", {}).get("user_id")
        transaction_id = session.get("id")

        if course_id and user_id:
            try:
                # Update Payment status
                payment = Payment.objects.get(
                    transaction_id=transaction_id,
                    user_id=user_id,
                    course_id=course_id
                )
                payment.status = Payment.STATUS_COMPLETED
                payment.save()

                # Create Enrollment
                Enrollment.objects.get_or_create(
                    student_id=user_id,
                    course_id=course_id,
                )
            except Payment.DoesNotExist:
                # In rare cases webhook fires before our create view finishes committing
                pass
