# Generated by Django 2.2.15 on 2020-09-14 20:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rain',
            old_name='quantity',
            new_name='milimeters',
        ),
    ]