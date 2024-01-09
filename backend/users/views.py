from djoser.views import UserViewSet
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from .models import User
from .serializers import UserSerializer


# from rest_framework.permissions import IsAuthenticated


class UserViewSet(UserViewSet):
    http_method_names = ["get", "post"]
    pagination_class = LimitOffsetPagination
    # permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
