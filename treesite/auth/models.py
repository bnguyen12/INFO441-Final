from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Permissions(models.Model):
    user_id = models.ForeignKey('User', null=True)
    ADMIN = "Admin"
    USER = "User"
    SELLER = "Seller"
    PERMISSION_TYPES = (
        (ADMIN, "Admin"),
        (USER, "User"),
        (SELLER, "Seller")
    )
    perm_type = models.CharField(
        max_length=5,
        choices= PERMISSION_TYPES,
        default = USER,
    )