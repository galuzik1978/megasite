# Generated by Django 3.1.1 on 2020-09-26 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='in_head_name',
        ),
    ]
