# Generated by Django 5.0.1 on 2024-02-07 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0005_alter_recipepostmodel_post_ingredients'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmodel',
            name='event_ima',
            field=models.ImageField(null=True, upload_to='images/event_img/'),
        ),
    ]
