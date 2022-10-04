from django.db import models

class CustomFieldContent(models.Model):
    user_custom_field = models.ForeignKey("UserCustomField", on_delete=models.CASCADE, related_name='field_content')
    contact = models.ForeignKey("Contact", on_delete=models.CASCADE, related_name='field_content')
    content = models.TextField()