# Generated by Django 5.0.3 on 2024-05-15 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xPloreBlog', '0037_alter_post_author_alter_post_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('1', 'Project Planning'), ('2', 'Stakeholder Management'), ('3', 'Resource Optimization'), ('4', 'Continuous Improvement'), ('5', 'Agile Project Management'), ('6', 'Project Management Office')], max_length=50, null=True),
        ),
    ]
