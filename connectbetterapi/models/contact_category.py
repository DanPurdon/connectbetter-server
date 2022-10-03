from django.db import models

class ContactCategory(models.Model):
    contact = models.ForeignKey("Contact", on_delete=models.CASCADE, related_name='contact_categories')
    user_category = models.ForeignKey("UserCategory", on_delete=models.CASCADE, related_name='user_categories')
    