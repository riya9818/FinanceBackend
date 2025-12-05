from django.db import models
from django.conf import settings
# Create your models here.

class Customer(models.Model):
    account_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_customers'
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    joined_date = models.DateField()
    is_active = models.BooleanField(default=True)
    country = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name