# Generated by Django 5.0.3 on 2024-05-15 07:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xPloreBlog', '0044_alter_post_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entity_type', models.CharField(default='Blog', max_length=50)),
                ('name', models.CharField(max_length=75, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('created_by', models.CharField(default=1, max_length=100)),
                ('created_on', models.DateField()),
                ('updated_by', models.CharField(default=1, max_length=100)),
                ('updated_on', models.DateField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='statuses', to='xPloreBlog.status'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='categories', to='xPloreBlog.category'),
        ),
    ]
