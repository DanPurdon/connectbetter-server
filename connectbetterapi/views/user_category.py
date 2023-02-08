"""View module for handling requests about User Categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from connectbetterapi.models import UserCategory
from django.db.models import Q

class UserCategoryView(ViewSet):
    """Categories view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single userCategory

        Returns:
            Response -- JSON serialized userCategory
        """
        try:
            userCategory = UserCategory.objects.get(pk=pk)
            serializer = CategoriesSerializer(userCategory)
            return Response(serializer.data)
        except UserCategory.DoesNotExist as ex:
            return Response({'userCategory': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get categories for current user

        Returns:
            Response -- JSON serialized list of categories
        """
        
        user = request.user
        categories = UserCategory.objects.filter(user_id=user.id)

        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized userCategory instance
        """
        user = request.user

        userCategory = UserCategory.objects.create(
            user=user,
            name=request.data["name"]
        )
        serializer = CategoriesSerializer(userCategory)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a userCategory

        Returns:
            Response -- Empty body with 204 status code
        """

        userCategory = UserCategory.objects.get(pk=pk)
        userCategory.name = request.data["name"]

        userCategory.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        userCategory = UserCategory.objects.get(pk=pk)
        userCategory.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CategoriesSerializer(serializers.ModelSerializer):
    """JSON serializer for categories
    """
    class Meta:
        model = UserCategory
        fields = ('id', 'user', 'name')
        depth = 1