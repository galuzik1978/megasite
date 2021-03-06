# Generated by Django 3.1.1 on 2021-02-10 08:31

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.fields.related


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0005_auto_20210202_2216'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sell',
            old_name='name',
            new_name='value',
        ),
        migrations.RemoveField(
            model_name='defectlist',
            name='document',
        ),
        migrations.RemoveField(
            model_name='defectlist',
            name='point',
        ),
        migrations.RemoveField(
            model_name='protocol',
            name='electric_measure',
        ),
        migrations.RemoveField(
            model_name='protocol',
            name='electric_template',
        ),
        migrations.RemoveField(
            model_name='protocol',
            name='enabled_measure',
        ),
        migrations.RemoveField(
            model_name='protocol',
            name='manual',
        ),
        migrations.RemoveField(
            model_name='protocol',
            name='num_control_not_use',
        ),
        migrations.RemoveField(
            model_name='protocol',
            name='ropes_brake',
        ),
        migrations.RemoveField(
            model_name='protocol',
            name='safe_exploitation',
        ),
        migrations.RemoveField(
            model_name='protocol',
            name='safety_device',
        ),
        migrations.RemoveField(
            model_name='protocol',
            name='unit_protection_valid',
        ),
        migrations.RemoveField(
            model_name='protocol',
            name='visual_inspection',
        ),
        migrations.AddField(
            model_name='defectlist',
            name='reason',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='organisation.reason', verbose_name='Документ'),
        ),
        migrations.AlterField(
            model_name='protocol',
            name='num',
            field=models.CharField(max_length=25, verbose_name='Номер протокола'),
        ),
        migrations.CreateModel(
            name='Rules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule', models.TextField(verbose_name='Определение правила на JS')),
                ('sell', models.ForeignKey(on_delete=django.db.models.fields.related.ForeignKey, to='organisation.sell')),
            ],
        ),
        migrations.CreateModel(
            name='RowDefects',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('defect', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organisation.defectlist')),
                ('row', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organisation.row')),
            ],
        ),
        migrations.CreateModel(
            name='ProtocolAnnex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.SmallIntegerField(choices=[(0, 'row'), (1, 'table'), (2, 'protocol')])),
                ('name', models.CharField(max_length=50, verbose_name='Имя файла')),
                ('file', models.FileField(upload_to='ProtocolAnnex')),
                ('sell_value', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='organisation.sellvalue')),
            ],
        ),
        migrations.CreateModel(
            name='ObservedDefect',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('defect', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organisation.defectlist')),
                ('sell_value', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='organisation.sellvalue')),
            ],
        ),
    ]
