# Generated by Django 5.0.1 on 2024-02-12 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0012_alter_reviewmodel_revw'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipepostmodel',
            name='post_description',
            field=models.CharField(max_length=800),
        ),
    ]