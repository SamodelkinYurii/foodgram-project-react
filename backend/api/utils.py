# from rest_framework.response import Response
# from rest_framework import permissions, status, viewsets
# from recipes.models import Recipe

# class AddDeleteMixin:
#     @staticmethod
#     def add(serializ, request, pk, metod):
#         current_user = request.user
#         serializer = serializ(
#             data={"recipe": pk, metod: current_user.id},
#             context={"request": request},
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
#     def delete(model, request, pk):
#         check_recipe = Recipe.objects.filter(id=pk)
#         check_favorite = model.objects.filter(
#             recipe=pk, check_favorite__id=request.user.id
#         )
#         if not check_recipe.exists():
#             return Response(
#                 {"detail": "Несуществующий рецепт"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         if check_favorite.exists():
#             check_favorite.delete()
#             return Response(
#                 {"detail": "Рецепт удален из избранного"},
#                 status=status.HTTP_204_NO_CONTENT,
#             )
#         return Response(
#             {"detail": "Рецепта нет в избранном"},
#             status=status.HTTP_400_BAD_REQUEST,
#         )

#         # current_user = request.user
#         # serializer = serializ(
#         #     data={"recipe": pk, metod: current_user.id},
#         #     context={"request": request},
#         # )
#         # serializer.is_valid(raise_exception=True)
#         # serializer.save()
#         # return Response(serializer.data, status=status.HTTP_201_CREATED)

#     # def delete_favorite(self, request, pk):
#     #     check_recipe = Recipe.objects.filter(id=pk)
#     #     current_user = self.request.user
#     #     check_favorite = FavoriteRecipe.objects.filter(
#     #         recipe=pk, favorite=current_user.id
#     #     )
#     #     if not check_recipe.exists():
#     #         return Response(
#     #             {"detail": "Несуществующий рецепт"},
#     #             status=status.HTTP_404_NOT_FOUND,
#     #         )
#     #     if check_favorite.exists():
#     #         check_favorite.delete()
#     #         return Response(
#     #             {"detail": "Рецепт удален из избранного"},
#     #             status=status.HTTP_204_NO_CONTENT,
#     #         )
#     #     return Response(
#     #         {"detail": "Рецепта нет в избранном"},
#     #         status=status.HTTP_400_BAD_REQUEST,
#     #     )