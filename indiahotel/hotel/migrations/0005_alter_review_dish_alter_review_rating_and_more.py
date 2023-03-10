# Generated by Django 4.1.2 on 2023-01-27 05:14

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hotel', '0004_alter_review_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.dish'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
