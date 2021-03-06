from __future__ import annotations

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,\
                                                        BaseUserManager
from django.conf import settings
from django.db.models.deletion import CASCADE

class UserManager(BaseUserManager):

    def __str__(self) -> str:
        return 'user_manager'
    
    def create_user(self, email, password=None, **extra_fields):
        """"Creates and saves a new user"""

        if not email:
            raise ValueError("A valid email is mandatory")
        user = self.model(email=self.normalize_email(email), **extra_fields) # for possible extra arguments
        user.set_password(password)
        user.save(using=self._db) # this is used when multiple databases are in place

        return user
    
    def create_superuser(self, email, password) -> 'user':
        """ Creates and saves a new superuser """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that support email instead of user name """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """ Tag to be used for a recipe """
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
    