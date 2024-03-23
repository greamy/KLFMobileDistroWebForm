# Generated by Django 5.0.1 on 2024-03-23 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebForm', '0005_submission'),
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placeholder', models.TextField()),
                ('required', models.BooleanField()),
                ('field_type', models.CharField(choices=[('TXT', 'text'), ('NUM', 'number'), ('EML', 'email'), ('OTH', 'other')], max_length=3)),
                ('visible', models.BooleanField()),
                ('order_num', models.IntegerField()),
                ('field_min', models.IntegerField(null=True)),
                ('field_max', models.IntegerField(null=True)),
            ],
        ),
    ]
