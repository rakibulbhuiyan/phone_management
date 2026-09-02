from rest_framework import serializers

from .models import Phone


class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phone
        fields = [
            "id",
            "name",
            "release_date",
            "display_size",
            "display_type",
            "processor",
            "ram",
            "storage",
            "battery",
            "main_camera",
            "selfie_camera",
            "operating_system",
            "source_url",
            "created_at",
            "updated_at",
        ]