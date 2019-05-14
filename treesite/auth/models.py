from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class permissions(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)

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

class user_posts(models.Model):
    tree_name = models.CharField(max_length=300, null=True)
    user_id = models.ForeignKey(User, null=True,  on_delete = models.CASCADE)
    description = models.CharField(max_length=1000)