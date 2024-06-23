# Generated by Django 5.0.3 on 2024-04-17 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xPloreBlog', '0005_project_p_background_project_p_core_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='excerpt',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='post',
            name='img_url',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='p_background',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='p_core_value',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='p_team',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
