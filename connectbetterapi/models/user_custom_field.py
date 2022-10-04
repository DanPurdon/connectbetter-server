from django.db import models
from django.conf import settings

class UserCustomField(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_categories')
    type = models.ForeignKey("FieldType", on_delete=models.CASCADE)
    name = models.CharField(max_length=75)