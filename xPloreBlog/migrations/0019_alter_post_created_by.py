# Generated by Django 5.0.3 on 2024-05-12 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xPloreBlog', '0018_alter_post_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_by',
            field=models.CharField(default='parmodchd', max_length=100, null=True),
        ),
    ]