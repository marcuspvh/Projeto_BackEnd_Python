# Generated by Django 4.1.5 on 2023-01-09 13:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("schedules", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="schedule",
            name="expire_date",
        ),
    ]
