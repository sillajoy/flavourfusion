# Generated by Django 5.0.1 on 2024-03-06 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0039_recipepostmodel_post_difficulty_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='user_email',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='user_phone',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
