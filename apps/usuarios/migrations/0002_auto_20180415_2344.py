# Generated by Django 2.0.3 on 2018-04-15 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fiscal',
            old_name='client',
            new_name='user',
        ),
    ]