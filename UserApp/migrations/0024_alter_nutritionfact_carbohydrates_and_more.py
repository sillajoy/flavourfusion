# Generated by Django 5.0.1 on 2024-02-28 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0023_alter_nutritionfact_fat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nutritionfact',
            name='carbohydrates',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='nutritionfact',
            name='fiber',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='nutritionfact',
            name='protein',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]