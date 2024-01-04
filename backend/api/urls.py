from django.urls import include, path, re_path
from rest_framework import routers
from djoser import views

from ingredients.views import IngredientViewSet
from tags.views import TagViewSet
from users.views import GetPostUserViewSet

# users = routers.DefaultRouter()
# users.register('users', views.UserViewSet)

router = routers.DefaultRouter()
router.register("tags", TagViewSet, basename="tags")
router.register("ingredients", IngredientViewSet, basename="ingredients")
router.register("users", GetPostUserViewSet, basename="users")


urlpatterns = [
    path("", include(router.urls)),
    # path('', include(users.urls)),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),
    # path('auth/', include('djoser.urls')),
]
