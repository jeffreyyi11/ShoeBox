# Generated by Django 2.2.4 on 2020-09-24 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0004_user_shoes_liked'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoe',
            name='liked',
            field=models.BooleanField(default=False),
        ),
    ]
