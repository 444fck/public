# Generated by Django 4.1.7 on 2023-04-08 03:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('function', '0004_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configuration',
            old_name='input_time',
            new_name='config',
        ),
        migrations.RenameField(
            model_name='configuration',
            old_name='first_name',
            new_name='firstname',
        ),
        migrations.RenameField(
            model_name='configuration',
            old_name='last_name',
            new_name='lastname',
        ),
    ]
