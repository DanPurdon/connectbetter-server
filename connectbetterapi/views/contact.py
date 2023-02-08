"""View module for handling requests about User Contacts"""
from django.http import HttpResponseServerError
from datetime import date, datetime
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from connectbetterapi.models import UserCustomField, FieldType, CustomFieldContent, UserCategory, Contact, ContactCategory
from django.db.models import Q

class ContactView(ViewSet):
    """Contacts view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single contact

        Returns:
            Response -- JSON serialized contact
        """
        try:
            contact = Contact.objects.get(pk=pk)
            serializer = ContactsSerializer(contact)
            return Response(serializer.data)
        except Contact.DoesNotExist as ex:
            return Response({'contact': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get contacts for current user

        Returns:
            Response -- JSON serialized list of contacts
        """
        
        user = request.user
        contacts = Contact.objects.filter(user_id=user.id)

        serializer = LeanContactsSerializer(contacts, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized contact instance
        """
        user = request.user

        contact = Contact.objects.create(
            user = user,
            first_name = request.data["first_name"],
            last_name = request.data["last_name"],
            metAt = request.data["metAt"],
            city = request.data["city"],
            birthday = request.data["birthday"],
            email = request.data["email"],
            phone = request.data["phone"],
            socials = request.data["socials"],
            notes = request.data["notes"],
            date_created = date.today()
        )
        serializer = ContactsSerializer(contact)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a contact

        Returns:
            Response -- Empty body with 204 status code
        """

        contact = Contact.objects.get(pk=pk)
        contact.name = request.data["name"]
        fieldType = FieldType.objects.get(pk=request.data["type"])
        contact.type = fieldType

        contact.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        contact = Contact.objects.get(pk=pk)
        contact.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ContactsSerializer(serializers.ModelSerializer):
    """JSON serializer for single contact details
    """
    class Meta:
        model = Contact
        fields = ('id', 'user', 'first_name', 'last_name', 'metAt', 'city', 'birthday',
        'email', 'phone', 'socials', 'notes', 'date_created', 'categories', 'field_content')
        depth = 2  

class LeanContactsSerializer(serializers.ModelSerializer):
    """JSON Lean serializer for contacts, for summarized Contacts list
    """
    class Meta:
        model = Contact
        fields = ('id', 'user', 'first_name', 'last_name', 'metAt', 'city', 'birthday',
        'email', 'phone', 'socials', 'notes', 'date_created')
        depth = 1  