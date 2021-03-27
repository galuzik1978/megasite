# Generated by Django 3.1.1 on 2021-02-17 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0009_remove_protocol_object_exam'),
        ('postoffice', '0006_auto_20210212_0917'),
    ]

    operations = [
        migrations.AddField(
            model_name='workrequest',
            name='protocol',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, to='organisation.protocol'),
        ),
    ]