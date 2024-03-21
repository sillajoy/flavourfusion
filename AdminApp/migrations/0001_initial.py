# Generated by Django 5.0.1 on 2024-02-06 08:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminModel',
            fields=[
                ('admin_id', models.AutoField(primary_key=True, serialize=False)),
                ('admin_username', models.CharField(max_length=50)),
                ('admin_password', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'admin_table',
            },
        ),
        migrations.CreateModel(
            name='AdsModel',
            fields=[
                ('ads_id', models.AutoField(primary_key=True, serialize=False)),
                ('ads_name', models.CharField(max_length=50)),
                ('ads_product_description', models.CharField(max_length=150)),
                ('ads_image', models.ImageField(upload_to='images/ads_img/')),
                ('ads_link', models.URLField()),
                ('ads_start_date', models.DateField()),
                ('ads_end_date', models.DateField()),
                ('ads_create_at', models.DateTimeField(auto_now_add=True)),
                ('admin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminApp.adminmodel')),
            ],
            options={
                'db_table': 'ads_table',
            },
        ),
    ]