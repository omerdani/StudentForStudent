# Generated by Django 5.0.2 on 2024-03-18 16:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('S4S', '0003_remove_post2_user_name_post2_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post2',
            name='display_name',
            field=models.CharField(default='UnknownName', max_length=100),
        ),
        migrations.AlterField(
            model_name='post2',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='S4S.userprofile'),
        ),
    ]
