# Generated by Django 3.1.1 on 2021-02-12 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0007_auto_20210210_1523'),
        ('postoffice', '0005_auto_20210210_1331'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workrequest',
            name='object',
        ),
        migrations.AddField(
            model_name='workrequest',
            name='object',
            field=models.ManyToManyField(to='organisation.Object'),
        ),
    ]