# Generated by Django 5.0.3 on 2024-04-19 05:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xPloreBlog', '0010_remove_author_first_name_remove_author_last_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auser', to=settings.AUTH_USER_MODEL),
        ),
    ]