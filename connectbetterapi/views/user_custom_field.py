"""View module for handling requests about User CustomFields"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from connectbetterapi.models import UserCustomField, FieldType
from django.db.models import Q

class UserCustomFieldView(ViewSet):
    """CustomFields view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single userCustomField

        Returns:
            Response -- JSON serialized userCustomField
        """
        try:
            userCustomField = UserCustomField.objects.get(pk=pk)
            serializer = CustomFieldsSerializer(userCustomField)
            return Response(serializer.data)
        except UserCustomField.DoesNotExist as ex:
            return Response({'userCustomField': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get customFields for current user

        Returns:
            Response -- JSON serialized list of customFields
        """
        
        user = request.user
        customFields = UserCustomField.objects.filter(user_id=user.id)

        serializer = CustomFieldsSerializer(customFields, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized userCustomField instance
        """
        user = request.user
        fieldType = FieldType.objects.get(pk=request.data["type"])

        userCustomField = UserCustomField.objects.create(
            user=user,
            type=fieldType,
            name=request.data["name"]
        )
        serializer = CustomFieldsSerializer(userCustomField)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a userCustomField

        Returns:
            Response -- Empty body with 204 status code
        """

        userCustomField = UserCustomField.objects.get(pk=pk)
        userCustomField.name = request.data["name"]
        fieldType = FieldType.objects.get(pk=request.data["type"])
        userCustomField.type = fieldType

        userCustomField.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        userCustomField = UserCustomField.objects.get(pk=pk)
        userCustomField.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CustomFieldsSerializer(serializers.ModelSerializer):
    """JSON serializer for customFields
    """
    class Meta:
        model = UserCustomField
        fields = ('id', 'user', 'type', 'name')
        depth = 1