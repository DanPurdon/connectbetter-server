from django.db import models
from django.conf import settings

class UserCategory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_categories')
    name = models.CharField(max_length=75)