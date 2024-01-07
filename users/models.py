from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.core.validators import MinLengthValidator, MaxLengthValidator


# Create your models here.


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(
        max_length=255,
        unique=True,
        blank=False,
        null=False,
    )
    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[
            UnicodeUsernameValidator(),
            MinLengthValidator(6),
            MaxLengthValidator(30)
        ],
    )

    # user_type = models.PositiveSmallIntegerField(default=3)

    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username


class Profile(models.Model):
    # CASCADE: if user is deleted, delete profile
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)  # add validator for no future dates
    image = models.ImageField(default='profile.jpg', upload_to='profile_pics')

    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} -> Profile'

    # override save method
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs

    # django-cleanup