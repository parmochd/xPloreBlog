# Generated by Django 5.0.3 on 2024-04-17 13:46

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xPloreBlog', '0004_alter_project_created_by_alter_project_updated_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='p_background',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='p_core_value',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='p_team',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='created_by',
            field=models.CharField(default='parmodchd', max_length=100),
        ),
        migrations.AlterField(
            model_name='author',
            name='updated_by',
            field=models.CharField(default='parmodchd', max_length=100),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_by',
            field=models.CharField(default='parmodchd', max_length=100),
        ),
        migrations.AlterField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(null=True, to='xPloreBlog.tag'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_by',
            field=models.CharField(default='parmodchd', max_length=100),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='comment',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='created_by',
            field=models.CharField(default='parmodchd', max_length=100),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='updated_by',
            field=models.CharField(default='parmodchd', max_length=100),
        ),
        migrations.AlterField(
            model_name='project',
            name='created_by',
            field=models.CharField(default='parmodchd', max_length=100),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_about',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='project',
            name='updated_by',
            field=models.CharField(default='parmodchd', max_length=100),
        ),
        migrations.AlterField(
            model_name='tag',
            name='caption',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='tag',
            name='created_by',
            field=models.CharField(default='parmodchd', max_length=100),
        ),
        migrations.AlterField(
            model_name='tag',
            name='updated_by',
            field=models.CharField(default='parmodchd', max_length=100),
        ),
    ]