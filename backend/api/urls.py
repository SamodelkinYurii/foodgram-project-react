from django.urls import include, path
from rest_framework import routers

from tags.views import TagViewSet
from ingredients.views import IngredientViewSet


router = routers.DefaultRouter()
router.register("tags", TagViewSet, basename="tags")
router.register("ingredients", IngredientViewSet, basename="ingredients")


urlpatterns = [
    path("", include(router.urls)),
]
