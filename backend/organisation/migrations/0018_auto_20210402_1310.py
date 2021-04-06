# Generated by Django 3.1.1 on 2021-04-02 08:10

from django.db import migrations


def init_forms(apps, schema_editor):
    # Выбираем из базы нужную форму
    Form = apps.get_model('organisation', 'Form')
    form = Form.objects.get(name="Пассажирский лифт")

    # Создаем новую таблицу и привязываем ее к форме
    Table = apps.get_model('organisation', 'Table')
    table = Table(
        name='Данные измерительного контроля испытания сопротивления изоляции электрических цепей и электрооборудования лифта'
    )
    table.save()
    table.form.add(form)

    # Определяеи мтолбцы заданной таблицы
    Header = apps.get_model('organisation', 'Header')
    header = Header(
        table=table,
        text='№ п/п',
        type=2,
        value=None,
        editable=False
    )
    header.save()
    header = Header(
        table=table,
        text='Наименование линий, электрических машин по проекту',
        value='name',
        editable=False
    )
    header.save()
    header = Header(
        table=table,
        text='Рабочее напряжение',
        value='voltage',
        editable=False
    )
    header.save()
    header = Header(
        table=table,
        text='Марка провода, кабеля',
        value='cable',
        editable=False
    )
    header.save()
    header = Header(
        table=table,
        text='кол-во жил, сечение провода, кабеля (мм2)',
        value='section',
        editable=False
    )
    header.save()
    header = Header(
        table=table,
        text='Напряжение мегаомметра, В',
        value='control_voltage',
        editable=False
    )
    header.save()
    header = Header(
        table=table,
        text='Допустимое сопротивление изоляции, МОм',
        value='perm_res',
        editable=False
    )
    header.save()
    header = Header(
        table=table,
        text='A-B',
        value='a-b',
        editable=True
    )
    header.save()
    header = Header(
        table=table,
        text='B-C',
        value='b-c',
        editable=True
    )
    header.save()
    header = Header(
        table=table,
        text='A-C',
        value='a-c',
        editable=True
    )
    header.save()
    header = Header(
        table=table,
        text='A-N',
        value='a-n',
        editable=True
    )
    header.save()
    header = Header(
        table=table,
        text='B-N',
        value='b-n',
        editable=True
    )
    header.save()
    header = Header(
        table=table,
        text='C-N',
        value='c-n',
        editable=True
    )
    header.save()
    header = Header(
        table=table,
        text='A-PE',
        value='a-pe',
        editable=True
    )
    header.save()
    header = Header(
        table=table,
        text='B-PE',
        value='b-pe',
        editable=True
    )
    header.save()
    header = Header(
        table=table,
        text='C-PE',
        value='c-pe',
        editable=True
    )
    header.save()
    header = Header(
        table=table,
        text='N-PE',
        value='n-pe',
        editable=True
    )
    header.save()

    # Сформируем массив, содержащий неизменные данные строк таблицы
    rows = [
        {
            'name':'От ВУ до 1 ВА',
            'voltage':'(380 В)',
            'cable':'ПВ1',
            'section':'4(1х4)',
            'control_voltage':'1000',
            'perm_res':'1',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
        {
            'name': 'От КВ и КБ до обмотки (Б)',
            'voltage': '(380 В)',
            'cable': 'ПВ1',
            'section': '3(1х4)',
            'control_voltage': '1000',
            'perm_res': '1',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
        {
            'name': 'От КМ и КН до обмотки (М)М1',
            'voltage': '(380 В)',
            'cable': 'ПВ1',
            'section': '3(1х4)',
            'control_voltage': '1000',
            'perm_res': '1',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
        {
            'name': 'От КМ и КВ до ЭмТ',
            'voltage': '(380 В)',
            'cable': 'ПВ1',
            'section': '2(1х2,5)',
            'control_voltage': '1000',
            'perm_res': '1',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
        {
            'name': 'Обмотка Б скорости М1',
            'voltage': '(380 В)',
            'cable': 'ПЭВ-1',
            'section': None,
            'control_voltage': '1000',
            'perm_res': '0,5',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
        {
            'name': 'Обмотка М скорости М1',
            'voltage': '(380 В)',
            'cable': 'ПЭВ-1',
            'section': None,
            'control_voltage': '1000',
            'perm_res': '0,5',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
        {
            'name': 'Обмотка ЭмТ',
            'voltage': '(220 В)',
            'cable': 'ПЭВ-1',
            'section': None,
            'control_voltage': '1000',
            'perm_res': '1',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
        {
            'name': 'От РОД и РЗД до Эл. дв. М2',
            'voltage': '(95 В)',
            'cable': 'ПВ1',
            'section': '3(1x2,5)',
            'control_voltage': '500',
            'perm_res': '1',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
        {
            'name': 'Обмотка эл. двигателя М2',
            'voltage': '(95 В)',
            'cable': 'ПЭВ-1',
            'section': None,
            'control_voltage': '1000',
            'perm_res': '0,5',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
        {
            'name': 'От ВАЗ (ПР1) до ТР1',
            'voltage': '(380 В)',
            'cable': 'ПВ1',
            'section': '3(1x2,5)',
            'control_voltage': '1000',
            'perm_res': '1',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
        {
            'name': 'От ТР1 до ВПЗ',
            'voltage': '(85 В)',
            'cable': 'ПВ1',
            'section': '3(1x2,5)',
            'control_voltage': '500',
            'perm_res': '1',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
        {
            'name': 'Обмотка ТР1 первичная',
            'voltage': '(380 В)',
            'cable': 'ПЭВ-1',
            'section': None,
            'control_voltage': '1000',
            'perm_res': '1',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
        {
            'name': 'Обмотка ТР1 вторичная',
            'voltage': '(95 В)',
            'cable': 'ПЭВ-1',
            'section': None,
            'control_voltage': '500',
            'perm_res': '1',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
        {
            'name': 'Обмотка ТР1 вторичная',
            'voltage': '(85 В)',
            'cable': 'ПЭВ-1',
            'section': None,
            'control_voltage': '500',
            'perm_res': '1',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
        {
            'name': 'Цепь управления',
            'voltage': '(-110 В)',
            'cable': 'КПЛ2',
            'section': '(12x0,5)',
            'control_voltage': '1000',
            'perm_res': '1',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
        {
            'name': 'От ПР2 до ТР3',
            'voltage': '(380 В)',
            'cable': 'ПВ-1',
            'section': '2(1x2,5)',
            'control_voltage': '1000',
            'perm_res': '1',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
        {
            'name': 'Обмотка ТР3 первичная',
            'voltage': '(380 В)',
            'cable': 'ПЭВ-1',
            'section': None,
            'control_voltage': '1000',
            'perm_res': '1',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
        {
            'name': 'Обмотка ТР3 вторичная',
            'voltage': '(24 В)',
            'cable': 'ПЭВ-1',
            'section': None,
            'control_voltage': '500',
            'perm_res': '1',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
        {
            'name': 'Цепи сигнализации',
            'voltage': '(24 В)',
            'cable': 'ПУВГ-1',
            'section': '18x0,5',
            'control_voltage': '500',
            'perm_res': '1',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
        {
            'name': 'Цепи освещения шахты',
            'voltage': '(220 В)',
            'cable': 'ПВ1',
            'section': '2(1x1,5)',
            'control_voltage': '1000',
            'perm_res': '1',
            'a-b': None,
            'b-c': None,
            'a-c': None,
            'a-n': None,
            'b-n': None,
            'c-n': None,
            'a-pe': None,
            'b-pe': None,
            'c-pe': None,
            'n-pe': None,
        },
    ]

    # Добавим несколько строк в таблицу
    Row = apps.get_model('organisation', 'Row')
    Sell = apps.get_model('organisation', 'Sell')
    for data_row in rows:
        row = Row(
            table=table,
            name=data_row['name']
        )
        row.save()
        for key, value in data_row.items():
            sell = Sell(
                row=row,
                text=value,
                value=key
            )
            sell.save()

class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0017_auto_20210327_1221'),
    ]

    operations = [
        migrations.RunPython(init_forms),
    ]
