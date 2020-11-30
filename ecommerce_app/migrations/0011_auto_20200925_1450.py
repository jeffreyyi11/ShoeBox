# Generated by Django 2.2.4 on 2020-09-25 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_app', '0010_auto_20200925_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoe',
            name='uploaded_by',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='shoes_owned', to='ecommerce_app.User'),
        ),
    ]
