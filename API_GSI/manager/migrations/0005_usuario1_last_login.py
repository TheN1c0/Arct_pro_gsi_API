# Generated by Django 5.1.2 on 2024-10-19 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0004_usuario1_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario1",
            name="last_login",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="last login"
            ),
        ),
    ]