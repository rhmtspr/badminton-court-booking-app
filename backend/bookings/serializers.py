from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = (
            "id",
            "user",
            "court",
            "booking_date",
            "start_time",
            "end_time",
            "status",
            "created_at",
        )

        read_only_fields = ("user", "status", "created_at")

    def validate(self, data):
        court = data["court"]
        booking_date = data["booking_date"]
        start_time = data["start_time"]
        end_time = data["end_time"]

        if start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")

        overlapping = Booking.objects.filter(
            court=court,
            booking_date=booking_date,
            start_time__lt=end_time,
            end_time__gt=start_time,
            status="CONFIRMED",
        ).exists()

        if overlapping:
            raise serializers.ValidationError("This time slot is already booked.")

        return data
