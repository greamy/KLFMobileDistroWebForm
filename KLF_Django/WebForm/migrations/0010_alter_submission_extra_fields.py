# Generated by Django 4.2.6 on 2024-03-29 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebForm', '0009_submission_extra_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='extra_fields',
            field=models.JSONField(default={}),
        ),
    ]
