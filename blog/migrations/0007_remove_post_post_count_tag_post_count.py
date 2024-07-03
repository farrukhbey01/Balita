# Generated by Django 5.0.2 on 2024-03-09 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_post_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_count',
        ),
        migrations.AddField(
            model_name='tag',
            name='post_count',
            field=models.IntegerField(default=0),
        ),
    ]
