import os
from django.core.exceptions import ValidationError

ALLOWED_EXTENSIONS = [".pdf", ".jpg", ".jpeg", ".png"]
MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB


def validate_document_file(uploaded_file):
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            f"Unsupported file extension: {ext}. Allowed: {ALLOWED_EXTENSIONS}"
        )
    if uploaded_file.size > MAX_UPLOAD_SIZE:
        raise ValidationError("File size exceeds maximum of 5MB.")
