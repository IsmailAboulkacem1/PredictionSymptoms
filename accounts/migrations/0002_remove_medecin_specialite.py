# Generated by Django 5.1.4 on 2024-12-31 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medecin',
            name='specialite',
        ),
    ]
