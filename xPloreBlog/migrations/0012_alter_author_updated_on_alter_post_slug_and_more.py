# Generated by Django 5.0.3 on 2024-04-20 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xPloreBlog', '0011_alter_author_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='updated_on',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='slug',
            field=models.SlugField(blank=True, default='', unique=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_on',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='updated_on',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='updated_on',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='reply',
            name='updated_on',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='updated_on',
            field=models.DateField(auto_now=True),
        ),
    ]