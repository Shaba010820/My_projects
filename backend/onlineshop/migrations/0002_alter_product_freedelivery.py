# Generated by Django 4.2.11 on 2024-10-16 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("onlineshop", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="freeDelivery",
            field=models.BooleanField(),
        ),
    ]
