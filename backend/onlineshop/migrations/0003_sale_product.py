# Generated by Django 4.2.11 on 2024-10-16 10:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("onlineshop", "0002_alter_product_freedelivery"),
    ]

    operations = [
        migrations.AddField(
            model_name="sale",
            name="product",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="onlineshop.product",
            ),
            preserve_default=False,
        ),
    ]