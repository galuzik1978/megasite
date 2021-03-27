from django.db import models
from django.contrib.auth.models import User


class TypeOrganisation(models.Model):
    name = models.CharField("Тип организации", max_length=255)

    def __str__(self):
        return self.name


class ChoiceName(models.Model):
    name = models.CharField("Имя поля", max_length=255)

    def __str__(self):
        return self.name


class FormType(models.Model):
    name = models.CharField("Программа обследования", max_length=255)

    def __str__(self):
        return self.name


class Element(models.Model):
    name = models.CharField("Контролируемый элемент", max_length=255)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField("Вид контроля", max_length=255)

    def __str__(self):
        return self.name


class CityType(models.Model):
    name = models.CharField("Вид населенного пункта", max_length=255)

    def __str__(self):
        return self.name


class StreetType(models.Model):
    name = models.CharField("Вид улицы", max_length=255)

    def __str__(self):
        return self.name


class TypeLift(models.Model):
    name = models.CharField("Вид улицы", max_length=255)

    def __str__(self):
        return self.name


class LiftDesign(models.Model):
    name = models.CharField("Вид улицы", max_length=255)

    def __str__(self):
        return self.name


class TypeProtocol(models.Model):
    name = models.CharField("Тип протокола", max_length=25)

    def __str__(self):
        return self.name


class DeviceSet(models.Model):
    name = models.CharField("Набор инструментов", max_length=25)

    def __str__(self):
        return self.name


class StatusDevice(models.Model):
    name = models.CharField("Статус устройства", max_length=25)

    def __str__(self):
        return self.name


class TypeDevice(models.Model):
    name = models.CharField("Тип устройства", max_length=25)

    def __str__(self):
        return self.name


class RangeMeasure(models.Model):
    name = models.CharField("Тип устройства", max_length=25)

    def __str__(self):
        return self.name


class AccuracyClass(models.Model):
    name = models.CharField("Класс точности", max_length=25)

    def __str__(self):
        return self.name


class Organisation(models.Model):
    inn = models.BigIntegerField(help_text="ИНН")
    inn_filial = models.BigIntegerField(help_text="ИНН филиала", blank=True, null=True)
    full_name = models.CharField(help_text="Полное название организации", max_length=255)
    type_customer = models.ForeignKey(TypeOrganisation, on_delete=models.CASCADE, help_text="Тип клиента")
    head = models.CharField(help_text="Должность руководителя",  max_length=100)
    head_name = models.CharField(help_text="Имя руководителя",  max_length=50)
    head_surname = models.CharField(help_text="Отчество руководителя",  max_length=50)
    head_last_name = models.CharField(help_text="Фамилия руководителя", max_length=50)
    kpp = models.BigIntegerField(help_text="КПП", blank=True, null=True)
    ogrn = models.BigIntegerField(help_text="ОГРН")
    bank = models.CharField(help_text="Наименование банка", max_length=200, blank=True, null=True)
    account = models.BigIntegerField(help_text="Расчетный счет", blank=True, null=True)
    cor_account = models.BigIntegerField(help_text="Кор.счёт", blank=True, null=True)
    bic = models.IntegerField(help_text="БИК", blank=True, null=True)
    phone = models.BigIntegerField(blank=True, null=True, help_text='Телефон')
    add_phone = models.BigIntegerField(blank=True, null=True, help_text='Доп. телефон')
    fax = models.BigIntegerField(blank=True, null=True, help_text="Факс")
    filial_count = models.SmallIntegerField(help_text="Кол-во филииалов", blank=True, null=True)
    legal_address = models.CharField(max_length=500, help_text="Юридический адрес", blank=True, null=True)
    post_address = models.CharField(max_length=500, help_text="Почтовый адрес", blank=True, null=True)

    def __str__(self):
        return self.full_name


class Object(models.Model):
    postcode = models.IntegerField("Почтовый индекс")
    region = models.CharField("Регион", max_length=100)
    city_type = models.ForeignKey(CityType, on_delete=models.CASCADE, verbose_name="Вид населенного пункта")
    city = models.CharField("Город", max_length=100)
    street_type = models.ForeignKey(StreetType, models.CASCADE, verbose_name="Вид улицы")
    street = models.CharField("Название",  max_length=100)
    building = models.CharField("Корпус", blank=True, null=True, max_length=50)
    entrance = models.IntegerField("Номер подъезда", blank=True, null=True,)
    office = models.CharField("Номер офиса", blank=True, null=True, max_length=25)
    lifts_count = models.SmallIntegerField("Кол-во лифтов", blank=True, null=True)
    reg_num = models.CharField("Регистрационный номер", max_length=25, blank=True, null=True)
    mf_year = models.DateField("Год выпуска", blank=True, null=True)
    type_lift = models.ForeignKey(TypeLift, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Тип лифта")
    capacity = models.DecimalField("Грузоподъемность", blank=True, null=True, max_digits=7, decimal_places=2)
    floors = models.SmallIntegerField("Кол-во этажей", blank=True, null=True)
    speed = models.DecimalField("Скорость лифта", blank=True, null=True, max_digits=6, decimal_places=3)
    maker = models.CharField("Производитель", max_length=100, blank=True, null=True)
    serial_number = models.CharField("Серийный номер", max_length=100, blank=True, null=True)
    date_exam = models.DateField("Дата проверки", blank=True, null=True)
    lift_design = models.ForeignKey(LiftDesign, models.CASCADE, verbose_name="Дизайн лифта", blank=True, null=True)
    freq = models.SmallIntegerField("частота", blank=True, null=True)
    auto_door = models.SmallIntegerField("Автоматические двери", blank=True, null=True)
    num_lines = models.SmallIntegerField("Кол-во линий", blank=True, null=True)
    customer = models.ForeignKey(Organisation, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return "{} {} {}".format(self.city,self.street, self.building)


class Form(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование формы")


class Protocol(models.Model):
    type_protocol = models.ForeignKey(TypeProtocol, on_delete=models.PROTECT, verbose_name="Тип протокола", null=True)
    num = models.CharField(max_length=25, verbose_name="Номер протокола", null=True)
    date_act = models.DateField(verbose_name="Год регистрации", auto_now=True)
    date_protocol = models.DateField(verbose_name="Год регистрации", auto_now=True)
    customer = models.ForeignKey(Organisation, on_delete=models.PROTECT, related_name="customer", verbose_name="Заказчик", null=True)
    owner = models.ForeignKey(Organisation, on_delete=models.PROTECT, related_name="owner", verbose_name="Собственник", null=True)
    worker = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Исполнитель", related_name="user", null=True)
    device_set = models.ForeignKey(DeviceSet, on_delete=models.PROTECT, verbose_name="Набор инструментов", null=True)
    customer_person = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Контактное лицо заказчика",
        related_name="customer_person",
        null = True
    )
    owner_person = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Контактное лицо собственника",
        related_name="owner_person",
        null=True
    )
    form = models.ForeignKey(Form, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return "{} от {}".format(self.num, self.date_act)


class Device(models.Model):
    name = models.CharField("Наименование прибора", max_length=50)
    type_device = models.ForeignKey(TypeDevice, on_delete=models.PROTECT, verbose_name="Тип прибора")
    serial_number = models.CharField("Серийный номер", max_length=25)
    state_reg = models.CharField(max_length=25)
    range_measure = models.ForeignKey(RangeMeasure, on_delete=models.PROTECT)
    accuracy_class = models.ForeignKey(AccuracyClass, on_delete=models.PROTECT)
    verify_number = models.CharField(max_length=25)
    verify_date = models.DateField(auto_now=True, verbose_name="Дата последней поверки")
    next_verify = models.DateField(verbose_name="Дата следующей поверки")
    period_verify = models.DurationField(verbose_name="Период поверки")
    certification_center = models.CharField(verbose_name="Сертификационный центр", max_length=25)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    device_set = models.ForeignKey(DeviceSet, on_delete=models.PROTECT)
    maker = models.CharField(max_length=50, verbose_name="Производитель")
    status = models.ForeignKey(StatusDevice, on_delete=models.PROTECT, verbose_name="Статус устройства")

    def __str__(self):
        return "{} от {} {}".format(self.num, self.date_act, self.object_exam)


class Document(models.Model):
    name = models.CharField(max_length=255, verbose_name="Документ")


class Reason(models.Model):
    document = models.ForeignKey(Document, on_delete=models.PROTECT)
    point = models.CharField(max_length=25,verbose_name="Номер пункта")
    phrasing = models.TextField()

    def __str__(self):
        return "Док. {} п. {}".format(
            self.document,
            self.point)


class DefectList(models.Model):
    reason = models.ForeignKey(Reason, on_delete=models.PROTECT, verbose_name="Документ", null=True)
    phrasing = models.TextField()

    def __str__(self):
        return "Док. {} п. {}".format(
            self.reason.document.name,
            self.phrasing
        )


class Table(models.Model):
    form = models.ManyToManyField(Form)
    name = models.CharField(max_length=255, verbose_name="Наименование таблицы")


class Header(models.Model):
    ALIGN_CHOICES = [
        (0, 'none'),
        (1, 'start'),
        (2, 'center'),
        (3, 'end'),
    ]
    FIELD_TYPES = [
        (0, 'none'),
        (1, 'bool'),
        (2, 'rows_num'),
        (3, 'select'),
        (4, 'actions')
    ]
    table = models.ForeignKey(Table, on_delete=models.PROTECT)
    text = models.CharField(max_length=255, verbose_name="Наименование столбца", blank=True, null=True)
    align = models.SmallIntegerField(choices=ALIGN_CHOICES, blank=True, null=True)
    type = models.SmallIntegerField(choices=FIELD_TYPES, blank=True, null=True)
    sortable = models.BooleanField(blank=True, null=True)
    value = models.CharField(max_length=255, verbose_name="Наименование данных столбца", blank=True, null=True)
    width = models.CharField(max_length=5, verbose_name="Относительная ширина столбца", blank=True, null=True)
    editable = models.BooleanField(blank=True, null=True)
    column = models.CharField(max_length=50, null=True)


class Row(models.Model):
    table = models.ForeignKey(Table, on_delete=models.PROTECT)
    name = models.CharField(max_length=255, verbose_name="Наименование строки")


class Sell(models.Model):
    row = models.ForeignKey(Row, on_delete=models.PROTECT)
    text = models.CharField(max_length=255, verbose_name="Неизменное содержимое ячейки", blank=True, null=True)
    value = models.CharField(max_length=255, null=True)


class SelectChoices(models.Model):
    header = models.ForeignKey(Header, on_delete=models.PROTECT)
    text = models.CharField(max_length=25)
    value = models.CharField(max_length=25)


class SellValue(models.Model):
    sell = models.ForeignKey(Sell, on_delete=models.PROTECT)
    protocol = models.ForeignKey(Protocol, on_delete=models.PROTECT)
    value = models.CharField(null=True, max_length=255, verbose_name="Содержимое ячейки")


# Список возможных дефектов для каждой строки протокола
class RowDefects(models.Model):
    table = models.ForeignKey(Table, on_delete=models.PROTECT)
    defect = models.ForeignKey(DefectList, on_delete=models.PROTECT)


# Список обнаруженных дефектов
class ObservedDefect(models.Model):
    sell_value = models.ForeignKey(SellValue, on_delete=models.PROTECT)
    defect = models.ForeignKey(DefectList, on_delete=models.PROTECT)


class Rules(models.Model):
    sell = models.ForeignKey(Sell, on_delete=models.ForeignKey)
    rule = models.TextField(verbose_name="Определение правила на JS")


class ProtocolAnnex(models.Model):
    protocol = models.ForeignKey(Protocol, on_delete=models.PROTECT)
    table = models.ForeignKey(Table,on_delete=models.PROTECT, null=True)
    row = models.ForeignKey(Row,on_delete=models.PROTECT, null=True)
    filename = models.CharField(max_length=50, verbose_name="Имя файла")
    file = models.FileField(upload_to="ProtocolAnnex")
