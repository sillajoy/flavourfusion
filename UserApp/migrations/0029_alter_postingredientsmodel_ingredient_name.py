# Generated by Django 5.0.1 on 2024-02-28 11:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0028_rename_ingreds_id_postingredientsmodel_ingredient_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postingredientsmodel',
            name='ingredient_name',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='UserApp.ingredientsmodel'),
        ),
    ]
