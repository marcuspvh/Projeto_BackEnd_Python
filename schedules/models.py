from django.db import models


class TypeChoices(models.TextChoices):
    CONSULTA = "Consulta"
    EXAME = "Exame"


class Schedule(models.Model):
    hour = models.TimeField()
    date = models.DateField()
    type = models.CharField(max_length=50, choices=TypeChoices.choices)
    description = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)
    cretead_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="schedules", null=True
    )
    doctor = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="doctor_schedules",
        null=True,
    )
