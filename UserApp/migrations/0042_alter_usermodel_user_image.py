# Generated by Django 5.0.1 on 2024-03-06 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0041_alter_usermodel_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='user_image',
            field=models.ImageField(upload_to='images/user_profile/'),
        ),
    ]