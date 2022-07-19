from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name = "email adress") #also a PK
    first_name = models.CharField(max_length=50, blank=True, default = "Person", verbose_name = "first name", help_text = "Please, enter your name")
    pocket = models.JSONField(verbose_name = "user pocket", default = dict) #name, quantity and amount of spend money for every item
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class CryptoData(models.Model):
    crypto_name = models.CharField(max_length=100, unique=True, primary_key=True, verbose_name = "id name of cryptocurrency") #also a PK
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name = "cost of cryptocurrency")
    human_name = models.CharField(max_length=50, unique=True,  verbose_name = "humanazed name of cryptocurrency") #readable name
    
    def __str__(self):
        return self.crypto_name