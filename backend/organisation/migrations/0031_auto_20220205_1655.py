# Generated by Django 3.1.1 on 2022-02-05 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0030_auto_20220205_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='ogrn',
            field=models.BigIntegerField(help_text='ОГРН', null=True),
        ),
    ]
