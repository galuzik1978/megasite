# Generated by Django 3.1.1 on 2022-02-05 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0028_auto_20220128_1404'),
    ]

    operations = [
        migrations.AddField(
            model_name='lead',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='organisation.leadstatus'),
        ),
    ]
