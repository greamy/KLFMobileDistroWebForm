# Generated by Django 4.2.6 on 2024-04-09 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebForm', '0011_alter_submission_extra_fields'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField()),
                ('email', models.TextField()),
            ],
        ),
    ]