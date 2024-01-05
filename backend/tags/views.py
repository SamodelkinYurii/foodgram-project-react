from rest_framework import permissions, viewsets

from .models import Tag
from .serializers import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
