# Generated by Django 5.0.3 on 2024-05-15 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xPloreBlog', '0047_alter_status_options_alter_category_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='auth_code',
            field=models.CharField(max_length=5),
        ),
    ]
