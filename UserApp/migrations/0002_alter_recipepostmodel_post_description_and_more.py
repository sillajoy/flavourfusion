# Generated by Django 5.0.1 on 2024-02-07 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipepostmodel',
            name='post_description',
            field=models.CharField(max_length=350),
        ),
        migrations.AlterField(
            model_name='recipepostmodel',
            name='post_procedure',
            field=models.CharField(max_length=400),
        ),
    ]
