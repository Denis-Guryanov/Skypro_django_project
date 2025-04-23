from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(
        upload_to="users/avatars/", null=True, blank=True, verbose_name="Аватар"
    )
    phone_number = PhoneNumberField(
        blank=True, null=True, verbose_name="Номер телефона"
    )
    country = CountryField(null=True, blank=True, verbose_name="Страна")
    token = models.CharField(
        max_length=100, verbose_name="токен", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
