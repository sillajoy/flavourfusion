# Generated by Django 5.0.1 on 2024-03-03 11:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0033_usermodel_user_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipePostViewModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view_count', models.IntegerField(default=0)),
                ('post', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='UserApp.recipepostmodel')),
            ],
            options={
                'db_table': 'recipe_post_view_table',
            },
        ),
    ]
