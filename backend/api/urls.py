from django.urls import include, path, re_path
from djoser import views
from rest_framework import routers

from ingredients.views import IngredientViewSet
from tags.views import TagViewSet
from users.views import UserViewSet
from recipes.views import RecipeViewSet


# users = routers.DefaultRouter()
# users.register('users', views.UserViewSet)

router = routers.DefaultRouter()
router.register("tags", TagViewSet, basename="tags")
router.register("ingredients", IngredientViewSet, basename="ingredients")
router.register("users", UserViewSet, basename="users")
router.register("recipes", RecipeViewSet, basename="recipes")



urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("djoser.urls.authtoken")),
    # path('auth/', include('djoser.urls.authtoken')),
    # path('', include(users.urls)),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),
    # path('auth/', include('djoser.urls')),
]
