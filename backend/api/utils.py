from rest_framework import status
from rest_framework.response import Response

from recipes.models import Recipe


class AddDelMixin:
    @staticmethod
    def create_entry(serializ, request, pk):
        current_user = request.user
        serializer = serializ(
            data={"recipe": pk, "user": current_user.id},
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def delete_entry(model, request, pk, fsc_metod):
        check_recipe = Recipe.objects.filter(id=pk)
        check_favorite = model.objects.filter(recipe=pk, user=request.user.id)
        if not check_recipe.exists():
            return Response(
                {"detail": "Несуществующий рецепт"},
                status=status.HTTP_404_NOT_FOUND,
            )
        if check_favorite.exists():
            check_favorite.delete()
            return Response(
                {"detail": f"Рецепт удален из {fsc_metod}"},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {"detail": f"Рецепта нет в {fsc_metod}"},
            status=status.HTTP_400_BAD_REQUEST,
        )
