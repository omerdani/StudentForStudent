# Generated by Django 5.0.2 on 2024-03-18 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('S4S', '0004_post2_display_name_alter_post2_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post2',
            name='display_name',
        ),
        migrations.RemoveField(
            model_name='post2',
            name='user',
        ),
        migrations.AddField(
            model_name='post2',
            name='user_name',
            field=models.CharField(default='none', max_length=100),
        ),
        migrations.AddField(
            model_name='post2',
            name='user_type',
            field=models.CharField(default='none', max_length=20),
        ),
    ]
