from django.db import models
from django.contrib.auth.models import AbstractUser


class Seasons(models.TextChoices):
    F = "F"
    M = "M"
    DEFAULT = "Not informed"


class User(AbstractUser):

    name = models.CharField(max_length=200)
    cpf = models.CharField(max_length=11, unique=True)
    age = models.IntegerField()
    sex = models.CharField(
        max_length=20,
        choices=Seasons.choices,
        default=Seasons.DEFAULT,
    )
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_doctor = models.BooleanField()
    phone_number = models.CharField(max_length=13)
    is_superuser = models.BooleanField(default=False)

    address = models.OneToOneField(
        "Address", on_delete=models.CASCADE, related_name="users"
    )

    info_doctor = models.ForeignKey(
        "Doctor_info", on_delete=models.CASCADE, related_name="users", null=True
    )


class Address(models.Model):
    district = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=15)
    number = models.CharField(max_length=13)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)


class Doctor_specialties(models.Model):
    name_specialties = models.CharField(max_length=200)


class Doctor_info(models.Model):
    crm = models.CharField(max_length=9, unique=True)
    specialties = models.ManyToManyField(
        Doctor_specialties,
        related_name="specialties",
    )
