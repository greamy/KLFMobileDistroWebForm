# Generated by Django 5.0.1 on 2024-03-23 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebForm', '0006_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='field_id',
            field=models.TextField(default='default'),
        ),
        migrations.AddField(
            model_name='field',
            name='name',
            field=models.TextField(default='default'),
        ),
        migrations.AddField(
            model_name='field',
            name='tefap',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='field_max',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='field',
            name='field_min',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
