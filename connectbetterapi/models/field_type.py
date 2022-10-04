from django.db import models

class FieldType(models.Model):
    type = models.CharField(max_length=50)