from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
# from djoser.views import UserViewSet as DjoserUserViewSet
from djoser.views import UserViewSet

from .models import Subscribe, User
from .paginations import LimitPageNumberPagination
from .serializers import UserSerializer


class UserViewSet(UserViewSet):
    http_method_names = ["get", "post"]
    pagination_class = PageNumberPagination
    # permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
