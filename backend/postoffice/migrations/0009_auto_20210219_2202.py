# Generated by Django 3.1.1 on 2021-02-19 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postoffice', '0008_auto_20210219_2113'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workrequest',
            old_name='object',
            new_name='object_req',
        ),
    ]