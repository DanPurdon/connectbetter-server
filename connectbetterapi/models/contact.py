from django.db import models
from django.conf import settings

class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_contacts')
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    notes = models.TextField()
    birthday = models.DateField()
    date_created = models.DateField()