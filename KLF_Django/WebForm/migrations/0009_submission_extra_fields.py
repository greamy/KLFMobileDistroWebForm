# Generated by Django 4.2.6 on 2024-03-29 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebForm', '0008_alter_field_field_id_alter_field_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='extra_fields',
            field=models.JSONField(default=''),
        ),
    ]