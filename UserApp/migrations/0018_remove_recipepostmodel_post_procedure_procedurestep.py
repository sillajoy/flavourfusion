# Generated by Django 5.0.1 on 2024-02-28 06:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0017_rename_username_usermodel_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipepostmodel',
            name='post_procedure',
        ),
        migrations.CreateModel(
            name='ProcedureStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_order', models.IntegerField()),
                ('step_text', models.TextField()),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='procedure_steps', to='UserApp.recipepostmodel')),
            ],
            options={
                'db_table': 'procedure_steps',
            },
        ),
    ]