from django.db import models
from django.contrib.auth.models import User

class TreeType(models.Model):
    breed = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=250)

class Trees(models.Model):
    tree_type_id = models.ForeignKey(TreeType, on_delete=models.CASCADE)
    age = models.IntegerField()
    AVAILABLE = 'AVAILABLE'
    SOLD = 'SOLD'
    PENDING = 'PENDING'
    STATUS_CHOICES = (
        (AVAILABLE, 'Available'),
        (PENDING, 'Sold'),
        (SOLD, 'Pending'),
    )

    status = models.CharField(
        max_length = 9,
        choices = STATUS_CHOICES,
        default = AVAILABLE
    )

class TreeAddress(models.Model):
    trees_id = models.ForeignKey(Trees, on_delete=models.CASCADE)
    street = models.CharField(max_length=250)
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=2)
    zip_code = models.IntegerField(default=98031)

class UserTrees(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    trees_id = models.ForeignKey(Trees, on_delete=models.CASCADE)

class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class InCart(models.Model):
    cart_id = models.IntegerField()
    trees_id = models.ForeignKey(Trees, on_delete=models.CASCADE)


class Permissions(models.Model):
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
        max_length=9,
        choices= PERMISSION_TYPES,
        default = USER,
    )

class UserPosts(models.Model):
    tree_name = models.CharField(max_length=300, null=True)
    user_id = models.ForeignKey(User, null=True,  on_delete = models.CASCADE)
    description = models.CharField(max_length=1000)