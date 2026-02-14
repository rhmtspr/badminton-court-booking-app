from django.forms import ValidationError
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Booking
from .serializers import BookingSerializer


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        with transaction.atomic():
            court = serializer.validated_data["court"]
            booking_date = serializer.validated_data["booking_date"]
            start_time = serializer.validated_data["start_time"]
            end_time = serializer.validated_data["end_time"]

            overlapping = Booking.objects.select_for_update().filter(
                court=court,
                booking_date=booking_date,
                start_time__lt=end_time,
                end_time__gt=start_time,
                status="CONFIRMED",
            )

            if overlapping.exists():
                raise ValidationError("This time slot is already booked")

            serializer.save(user=self.request.user)

    @action(detail=True, methods=["patch"])
    def cancel(self, request, pk=None):
        booking = self.get_object()

        if booking.status == "CANCELLED":
            return Response({"detail": "Booking already cancelled."})

        booking.status = "CANCELLED"
        booking.save()

        return Response({"detail": "Booking cancelled successfully"})
