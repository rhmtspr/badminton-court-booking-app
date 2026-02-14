from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Court
from .serializers import CourtSerializer


class CourtViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Court.objects.filter(is_active=True)
    serializer_class = CourtSerializer
    permission_classes = [AllowAny]
