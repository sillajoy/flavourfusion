# Generated by Django 5.0.1 on 2024-02-28 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0019_procedurestep_step_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='procedurestep',
            name='step_name',
        ),
    ]
