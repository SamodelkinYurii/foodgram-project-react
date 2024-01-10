from djoser.views import UserViewSet
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from .models import User, Subscribe
from .serializers import UserSerializer, SubscribeSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action



# from rest_framework.permissions import IsAuthenticated


class UserViewSet(UserViewSet):
    # http_method_names = ["get", "post", "delete"]
    pagination_class = LimitOffsetPagination
    # permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=('GET',),
            permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request, id):
        pass

    @action(detail=True, methods=('POST',),
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, id):
        current_user = self.request.user
        serializer = SubscribeSerializer(
            data={'user': current_user.id, 'subscriber': id},
            context={'request': request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
  
    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        current_user = self.request.user
        check_subscribe = Subscribe.objects.filter(user=current_user, subscriber=id)
        if check_subscribe.exists():
            check_subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
