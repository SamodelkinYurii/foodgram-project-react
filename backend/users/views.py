from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .models import Subscribe, User
from .serializers import (
    SubscribeSerializer,
    SubscriptionSerializer,
    UserSerializer,
)


class UserViewSet(UserViewSet):
    pagination_class = LimitOffsetPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "me":
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    @action(
        detail=True,
        methods=("GET",),
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscriptions(self, request):
        current_user = get_object_or_404(User, username=request.user)
        subscribtions_list = current_user.user.all()
        page = self.paginate_queryset(subscribtions_list)
        serializer = SubscriptionSerializer(
            page,
            many=True,
            context={"request": request},
        )
        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=("POST",),
        permission_classes=[permissions.IsAuthenticated],
    )
    def subscribe(self, request, id):
        check_user = User.objects.filter(id=id)
        current_user = self.request.user
        check_subscribe = Subscribe.objects.filter(
            user=current_user, subscriber=id
        )
        if check_subscribe.exists():
            return Response(
                {"detail": "Вы уже подписанны на данного автора"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not check_user.exists():
            return Response(
                {"detail": "Нельзя подписатся на несуществующего автора"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = SubscribeSerializer(
            data={"user": current_user.id, "subscriber": id},
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        check_user = User.objects.filter(id=id)
        current_user = self.request.user
        check_subscribe = Subscribe.objects.filter(
            user=current_user, subscriber=id
        )
        if not check_user.exists():
            return Response(
                {"detail": "Нельзя отписатся от несуществующего автора"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if check_user.exists():
            if check_subscribe.exists():
                check_subscribe.delete()
                return Response({"detail": "Вы отписались от автора"}, status=status.HTTP_204_NO_CONTENT)
            return  Response({"detail": "Вы уже отписаны от автора"}, status=status.HTTP_400_BAD_REQUEST)
