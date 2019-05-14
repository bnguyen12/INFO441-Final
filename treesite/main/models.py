from django.db import models
from django.contrib.auth.models import User

class TreeType(models.Model):
    breed = models.CharField(max_length=250, unique=True)
    description = models.CharField(max_length=250)

class Trees(models.Model):
    tree_type_id = models.ForeignKey(TreeType, on_delete=models.CASCADE)
    age = models.IntegerField()
    
    NORMAL = 'NRML'
    SELLER = 'SLR'
    ADMIN = 'ADMIN'
    STATUS_CHOICES = (
        (SELLER, 'Seller'),
        (NORMAL, 'Normal'),
        (ADMIN, 'Admin'),
    )

    status = models.CharField(
        max_length = 5,
        choices = STATUS_CHOICES,
        default = NORMAL
    )

class TreeAddress(models.Model):
    trees_id = models.ForeignKey(Trees, on_delete=models.CASCADE)
    street = models.CharField(max_length=250)
    city = models.CharField(max_length=32)
    zip = models.IntegerField()

class Cart(models.Model):
    in_cart_id = models.ForeignKey('InCart', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class InCart(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    trees_id = models.ForeignKey(Trees, on_delete=models.CASCADE)