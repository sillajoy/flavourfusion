# Generated by Django 5.0.1 on 2024-02-28 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0030_alter_postingredientsmodel_ingredient_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='postingredientsmodel',
            name='ingredients_for',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
