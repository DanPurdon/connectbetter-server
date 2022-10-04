from django.db import models
from django.conf import settings

class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_contacts')
    first_name = models.CharField(max_length=75, blank=True)
    last_name = models.CharField(max_length=75, blank=True)
    metAt = models.CharField(max_length=150, blank=True)
    city = models.CharField(max_length=75, blank=True)
    birthday = models.DateField(null=True, blank=True)
    email = models.CharField(max_length=75, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    socials = models.CharField(max_length=150, blank=True)
    notes = models.TextField(blank=True)
    date_created = models.DateField()
    categories = models.ManyToManyField("UserCategory", through="ContactCategory", related_name="contact_categories")