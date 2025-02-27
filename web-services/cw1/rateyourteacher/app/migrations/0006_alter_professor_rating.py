# Generated by Django 4.2.19 on 2025-02-26 14:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_professor_rating_alter_rating_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='rating',
            field=models.FloatField(editable=False, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
