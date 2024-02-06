# Generated by Django 4.2.6 on 2024-02-06 17:32

from django.db import migrations, models
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('WebForm', '0003_rename_site_name_site_name'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='site',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), models.F('location'), name='unique_name_location'),
        ),
    ]
