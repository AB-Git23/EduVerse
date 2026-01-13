from rest_framework import serializers
from .models import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = [
            "id",
            "course",
            "enrolled_at",
        ]
        read_only_fields = ["id", "enrolled_at"]


