# Generated by Django 5.1.2 on 2024-10-19 01:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("manager", "0008_alter_usuario1_is_superuser"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="usuario1",
            options={
                "permissions": [
                    ("can_view_user", "Puede ver usuario"),
                    ("can_edit_user", "Puede editar usuario"),
                ]
            },
        ),
    ]
