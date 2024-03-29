import json
from abc import ABC

from dadata import Dadata
import requests
from django.contrib.auth.models import User
from django.db.models import Max
from django.utils.datetime_safe import datetime
from rest_framework import serializers, status, authentication, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from organisation.models import Organisation, TypeOrganisation, CityType, StreetType, TypeLift, LiftDesign, \
    TypeProtocol, DeviceSet, StatusDevice, TypeDevice, RangeMeasure, AccuracyClass, Object, Protocol, Device, Form, \
    Table, Header, Row, Sell, Lead
from mainWork.models import Status, TaskStatus, EventType, MainWork, Task, Message
from postoffice.models import Inbox, Outbox, TypeLetter, SendStatus, TypeWork, Contract, ContractStatus, WorkRequest, \
    ObjRequest
from user_profile.models import Profile, Role
from util.customize import Company_INN, Company_Phone

token = 'e01d0b0411274cc94fd22aa9c2bf5bf5d9f14936' # "Replace with Dadata API key"
secret = '29a8f7d7d8528121a4ecdeddc9796dc68d1c40f5' # "Replace with Dadata secret key"


def get_organization_by_inn(inn, request):
    dadata = Dadata(token)
    result = dadata.suggest("party", inn)
    url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/party"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Token {}".format(token)
    }
    data = {"query": inn}
    r = requests.post(url, headers=headers, json=data)
    try:
        res = r.json()['suggestions'][0]['data']
        try:
            type_customer = TypeOrganisation.objects.get(name=res['opf']['full'])
        except TypeOrganisation.DoesNotExist:
            type_customer = TypeOrganisation.objects.create(name=res['opf']['full'])

        if res['type'] == 'LEGAL':
            head_name = res['management']['name'].split()
            data = {
                'full_name': res['name']['short_with_opf'],
                'head': res['management']['post'],
                'head_name': head_name[1],
                'head_surname': head_name[2],
                'head_last_name': head_name[0],
                'kpp': res['kpp'],
                'ogrn': res['ogrn'],
                'inn': res['inn'],
                'address': res['address']['unrestricted_value'],
                'type_customer': TypeCustomerSer(type_customer, context={'request': request}).data
                # {"id":type_customer.pk,"name":type_customer.name}
            }
        elif res['type'] == 'INDIVIDUAL':
            head_name = res['name']['full'].split()
            data = {
                'full_name': res['name']['short_with_opf'],
                'head': res['opf']['full'],
                'head_name': head_name[1],
                'head_surname': head_name[2],
                'head_last_name': head_name[0],
                'kpp': '',
                'ogrn': res['ogrn'],
                'inn': res['inn'],
                'address': res['address']['unrestricted_value'],
                'type_customer': TypeCustomerSer(type_customer, context={'request': request}).data
            }
        else:
            raise Exception("Не известная форма собственности: {}".format(res['type']))
        response_status = status.HTTP_200_OK
        data['len'] = len(r.json()['suggestions'])
    except IndexError:
        data = "Проверьте ИНН. ИНН не найден в базе"
        response_status = status.HTTP_404_NOT_FOUND

    return Response(data, status=response_status)


def hint_address(address_string, request):
    url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Token {}".format(token)
    }
    data = {"query": address_string}
    r = requests.post(url, headers=headers, json=data)
    try:
        res = r.json()['suggestions'][0]
        response_status = status.HTTP_200_OK
        data['postcode'] = res['data']['postal_code']
        data['country'] = res['data']['country']
        data['region'] = res['data']['region_with_type']
        data['city_type'] = res['data']['city_type_full']
        data['city'] = res['data']['city']
        data['street_type'] = res['data']['street_type_full']
        data['street'] = res['data']['street']
        data['building'] = res['data']['house']
        data['address'] = res['unrestricted_value']

    except IndexError:
        data['error'] = "Проверьте адрес. Адрес не найден в базе"
        response_status = status.HTTP_404_NOT_FOUND

    return Response(data, status=response_status)


def get_name(data):
    name = {
        'name': None,
        'surname': None,
        'lastname': None
    }
    if data.get('management'):
        tmp = data['management'].get('name').split()
        name['name'] = tmp[1]
        name['surname'] = tmp[2] if len(tmp) >2  else ''
        name['lastname'] = tmp[0]
    elif data.get('fio'):
        name['name'] = data['fio']['name']
        name['surname'] = data['fio']['patronymic']
        name['lastname'] = data['fio']['surname']
    return name


def get_dadata_bank(bank, request):
    dadata = Dadata(token)
    result = dadata.suggest("bank", bank)
    if len(result) == 0:
        res = "Проверьте реквизиты банка. Банк не найден в базе"
        response_status = status.HTTP_404_NOT_FOUND
    else:
        res = [{
            'desc': "{}, БИК {}, ИНН {}".format(r['value'], r['data']['bic'], r['data']['inn']),
            'name': r['value'],
            'bic': r['data']['bic'],
            'inn': r['data']['inn'],
            'kpp': r['data']['kpp'],
            'correspondent_account': r['data']['correspondent_account']
        } for r in result]
        response_status = status.HTTP_200_OK
    return Response(res, status=response_status)


def get_dadata(inn, request):
    dadata = Dadata(token)
    result = dadata.suggest("party", inn, count=20)

    if len(result) == 0:
        res = "Проверьте ИНН. ИНН не найден в базе"
        response_status = status.HTTP_404_NOT_FOUND
    else:
        res = [{
            'desc': '{}, {}. {}, {}'.format(
                r['data']['inn'],
                r['data']['address']['data']['city_type'],
                r['data']['address']['data']['city'],
                r['value']),
            'inn': r['data']['inn'],
            'kpp': r['data'].get('kpp', None),
            'ogrn': r['data']['ogrn'],
            'phone': r['data']['phones'],
            'email': r['data']['emails'],
            'full_name': r['data']['name']['full'],
            'type_customer': r['data']['opf']['short'],
            'head': r['data']['management']['post'] if r['data'].get('management') else r['data']['opf']['full'],
            'head_name': get_name(r['data'])['name'],
            'head_surname': get_name(r['data'])['surname'],
            'head_lastname': get_name(r['data'])['lastname'],
            'legal_address': r['data']['address']['value']
        } for r in result]
        response_status = status.HTTP_200_OK
    return Response(res, status=response_status)


def header_sort(data):
    return data['order']


def row_sort(data):
    return data['row_order']


class TypeCustomerSer(serializers.ModelSerializer):

    class Meta:
        model = TypeOrganisation
        fields = '__all__'


class RoleSer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class OrganisationSer(serializers.ModelSerializer):
    type_customer = TypeCustomerSer()

    class Meta:
        model = Organisation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(OrganisationSer, self).__init__(*args, **kwargs)


class ProfileSer(serializers.ModelSerializer):
    organisation = OrganisationSer()
    role = RoleSer()

    class Meta:
        model = Profile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(ProfileSer, self).__init__(*args, **kwargs)

    def validate_user(self, value):
        return value


class UserSer(serializers.ModelSerializer):
    profile = ProfileSer(required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'profile']


class SenderSer(serializers.ModelSerializer):
    profile = ProfileSer(required=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'profile']

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(SenderSer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        user_data = {
            'username': self.initial_data['email'],
            'first_name': self.initial_data['first_name'],
            'last_name': self.initial_data['last_name'],
            'email': self.initial_data['email'],
        }
        role_pk = json.loads(self.initial_data['profile.role'])['id']
        role = Role.objects.get(pk=role_pk)
        customer_pk = json.loads(self.initial_data['profile.organisation'])['id']
        customer = Organisation.objects.get(pk=customer_pk)
        user = User(** user_data)
        user.save()
        user.profile.surname = self.initial_data['profile.surname']
        user.profile.phone = self.initial_data['profile.phone']
        user.profile.organisation = customer
        user.profile.role = role
        user.save()
        return user


class ManagerSer(serializers.ModelSerializer):
    profile = ProfileSer(required=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'profile']

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(ManagerSer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        user_data = {
            'username': self.initial_data['username'],
            'first_name': self.initial_data['first_name'],
            'last_name': self.initial_data['name'],
            'is_staff': True
        }
        try:
            role = Role.objects.get(name='Менеджер')
        except Role.DoesNotExist as err:
            role = Role.objects.create(name='Менеджер')
        try:
            customer = Organisation.objects.get(inn=Company_INN)
        except Organisation.DoesNotExist as err:
            organisation_data = get_organization_by_inn(Company_INN, None)
            type_customer = TypeOrganisation.objects.get(name=organisation_data.data['type_customer']['name'])
            customer = Organisation.objects.create(
                inn=organisation_data.data['inn'],
                full_name=organisation_data.data['full_name'],
                type_customer=type_customer,
                head=organisation_data.data['head'],
                head_name=organisation_data.data['head_name'],
                head_surname=organisation_data.data['head_surname'],
                head_last_name=organisation_data.data['head_last_name'],
                kpp=organisation_data.data['kpp'],
                ogrn=organisation_data.data['ogrn'],
                phone=Company_Phone
            )
        user = User(** user_data)
        user.save()
        user.profile.surname = self.initial_data['profile.surname']
        user.profile.organisation = customer
        user.profile.role = role
        user.save()
        return user


class MyTypeCustomerSer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class TypeWorkSer(serializers.ModelSerializer):
    class Meta:
        model = TypeWork
        fields = '__all__'


class CustomerSer(serializers.ModelSerializer):
    type_customer = TypeCustomerSer()

    class Meta:
        model = Organisation
        fields = [
            'id', 'inn', 'inn_filial', 'full_name', 'type_customer', 'head',
            'head_name', 'head_surname', 'head_last_name', 'kpp', 'ogrn',
            'phone', 'add_phone', 'fax', 'bic', 'bank', 'account', 'cor_account', 'legal_address', 'post_address'
        ]

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(CustomerSer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        pk = json.loads(self.initial_data['type_customer'])['id']
        type_customer = TypeOrganisation.objects.get(pk=pk)
        validated_data['type_customer'] = type_customer
        res = super(CustomerSer, self).create(validated_data)
        return res

    def __call__(self, value):
        res = super(CustomerSer, self).__call__(value)
        return res

class SendStatusSer(serializers.ModelSerializer):
    class Meta:
        model = SendStatus
        fields = ['id', 'name']


class TypeLetterSer(serializers.ModelSerializer):
    class Meta:
        model = TypeLetter
        fields = '__all__'


class InboxSer(serializers.ModelSerializer):
    sender = SenderSer(required=False, read_only=True)
    customer = CustomerSer(required=False, read_only=True)
    receiver = SenderSer(required=False, read_only=True)
    send_status = SendStatusSer(required=False, read_only=True)
    type_work = TypeWorkSer(required=False, read_only=True)
    type_letter = TypeLetterSer(required=False, read_only=True)
    num = serializers.IntegerField(required=False, read_only=True)

    class Meta:
        model = Inbox
        fields = ['id', 'num', 'date', 'sender', 'customer', 'title', 'content', 'type_letter', 'annex',
                  'send_status', 'type_work', 'notice', 'receiver']

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(InboxSer, self).__init__(*args, **kwargs)

    def update(self, instance, validated_data):

        for attr, value in self.initial_data.lists():
            try:
                data = json.loads(value[0])
                # data = data['id']
                value = instance.__getattribute__(attr).__class__.objects.get(pk=data['id'])
                setattr(instance, attr, value)
            except AttributeError as err:
                setattr(instance, attr, data)
        instance.save()
        return instance

    def create(self, validated_data):
        sender = User.objects.get(pk=json.loads(self.initial_data['sender'])['id'])
        try:
            num = Inbox.objects.all().aggregate(Max('num'))['num__max'] + 1
        except TypeError as err:
            num = 1
        customer = sender.profile.organisation
        send_status = SendStatus.objects.get(pk=json.loads(self.initial_data['send_status'])['id'])
        type_work = TypeWork.objects.get(pk=json.loads(self.initial_data['type_work'])['id'])
        try:
            type_letter = TypeLetter.objects.get(name="Новая заявка")
        except TypeLetter.DoesNotExist as err:
            type_letter = TypeLetter.objects.create(name="Новая заявка")
        try:
            annex = validated_data['annex']
        except KeyError as err:
            annex = None
        user = self.context['request'].user
        inbox_data = {
            'num': num,
            'date': datetime.now(),
            'sender': sender,
            'customer': customer,
            'title': self.initial_data['title'],
            'content': self.initial_data['content'],
            'type_letter': type_letter,
            'annex': annex,
            'send_status': send_status,
            'type_work': type_work,
            'receiver': user
        }
        inbox = Inbox(** inbox_data)
        inbox.save()
        return inbox


class OutboxSer(serializers.ModelSerializer):
    class Meta:
        model = Outbox
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(OutboxSer, self).__init__(*args, **kwargs)


class StatusSer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


class TaskStatusSer(serializers.ModelSerializer):
    class Meta:
        model = TaskStatus
        fields = '__all__'


class EventTypeSer(serializers.ModelSerializer):
    class Meta:
        model = EventType
        fields = '__all__'


class MainWorkSer(serializers.ModelSerializer):
    class Meta:
        model = MainWork
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(MainWorkSer, self).__init__(*args, **kwargs)


class TaskSer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(TaskSer, self).__init__(*args, **kwargs)


class MessageSer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class CityTypeSer(serializers.ModelSerializer):
    class Meta:
        model = CityType
        fields = '__all__'


class StreetTypeSer(serializers.ModelSerializer):
    class Meta:
        model = StreetType
        fields = '__all__'


class TypeLiftSer(serializers.ModelSerializer):
    class Meta:
        model = TypeLift
        fields = '__all__'


class LiftDesignSer(serializers.ModelSerializer):
    class Meta:
        model = LiftDesign
        fields = '__all__'


class TypeProtocolSer(serializers.ModelSerializer):
    class Meta:
        model = TypeProtocol
        fields = '__all__'


class DeviceSetSer(serializers.ModelSerializer):
    class Meta:
        model = DeviceSet
        fields = '__all__'


class StatusDeviceSer(serializers.ModelSerializer):
    class Meta:
        model = StatusDevice
        fields = '__all__'


class TypeDeviceSer(serializers.ModelSerializer):
    class Meta:
        model = TypeDevice
        fields = '__all__'


class RangeMeasureSer(serializers.ModelSerializer):
    class Meta:
        model = RangeMeasure
        fields = '__all__'


class AccuracyClassSer(serializers.ModelSerializer):
    class Meta:
        model = AccuracyClass
        fields = '__all__'


class ObjectSer(serializers.ModelSerializer):
    city_type = CityTypeSer()
    street_type = StreetTypeSer()
    lift_design = LiftDesignSer()
    mf_year = serializers.DateField(format="%Y")
    date_exam = serializers.DateField(format="%Y-%m")
    type_lift = TypeLiftSer()
    address = serializers.SerializerMethodField('get_address')
    form = serializers.SerializerMethodField('get_form')

    class Meta:
        model = Object
        fields = (
            'id',
            'postcode',
            'region',
            'city_type',
            'city',
            'street_type',
            'street',
            'building',
            'reg_num',
            'mf_year',
            'type_lift',
            'capacity',
            'floors',
            'date_exam',
            'address',
            'lift_design',
            'form'
        )

    def get_address(self, work_object):
        str = "{}. {}, {}. {}, д. {}".format(
            work_object.city_type.name[0],
            work_object.city,
            work_object.street_type.name[0:2],
            work_object.street,
            work_object.building
        )
        return str

    def get_form(self, work_object):
        if len(work_object.workrequest_set.all())>0:
            return FormsSer(work_object.workrequest_set.get().form).data
        else:
            return None

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(ObjectSer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        city_type = CityType.objects.get(pk=json.loads(self.initial_data['city_type'])['id'])
        street_type = StreetType.objects.get(pk=json.loads(self.initial_data['street_type'])['id'])
        lift_design = LiftDesign.objects.get(pk=json.loads(self.initial_data['lift_design'])['id'])
        object = Object.objects.create(
            postcode=self.initial_data['postcode'],
            region = self.initial_data['region'],
            city_type = city_type,
            city = self.initial_data['city'],
            street_type = street_type,
            street = self.initial_data['street'],
            building = self.initial_data['building'],
            lifts_count = self.initial_data['lifts_count'],
            reg_num = self.initial_data['reg_num'],
            mf_year = self.initial_data['mf_year'],
            capacity = self.initial_data['capacity'],
            floors = self.initial_data['floors'],
            speed = self.initial_data['speed'],
            maker = self.initial_data['maker'],
            serial_number = self.initial_data['serial_number'],
            date_exam = self.initial_data['date_exam'],
            lift_design = lift_design,
            freq = self.initial_data['freq'],
            num_lines = self.initial_data['num_lines'],
        )
        return object

    def update(self, instance, validated_data):

        for attr, value in self.initial_data.lists():
            try:
                data = json.loads(value[0])
                # data = data['id']
                value = instance.__getattribute__(attr).__class__.objects.get(pk=data['id'])
                setattr(instance, attr, value)
            except AttributeError as err:
                setattr(instance, attr, data)
        instance.save()
        return instance


class DeviceSer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(DeviceSer, self).__init__(*args, **kwargs)


class UserAuthSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


def validate(self, attrs):
    res = super(CustomerSer, self).validate(attrs)
    return res


def validate_inn(attrs):
    return attrs


class ContractSer(serializers.ModelSerializer):
    customer = CustomerSer()
    inbox = InboxSer()
    type_work = TypeWorkSer()
    # object = ObjectSer()

    class Meta:
        model = Contract
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(ContractSer, self).__init__(*args, **kwargs)

    def create(self, validated_data):
        inbox = Inbox.objects.get(pk=json.loads(self.initial_data['inbox'])['id'])
        customer = inbox.customer
        # unit = Object.objects.get(pk=json.loads(self.initial_data['object'])['id'])
        # unit.customer = customer
        type_work = TypeWork.objects.get(pk=json.loads(self.initial_data['type_work'])['id'])
        # unit.save()
        date = datetime.strptime(self.initial_data['date'],"%Y-%m-%d")
        end_date = datetime.strptime(self.initial_data['end_date'],"%Y-%m-%d")
        try:
            num = Contract.objects.all().aggregate(Max('num'))['num__max'] + 1
        except TypeError as err:
            num = 1

        init_status = "Новый договор"
        try:
            status = ContractStatus.objects.get(name=init_status)
        except ContractStatus.DoesNotExist as err:
            status = ContractStatus.objects.create(name=init_status)
        contract = Contract.objects.create(
            num=num,
            date=date.date(),
            end_date=end_date.date(),
            type_work=type_work,
            cost=self.initial_data['cost'],
            external_num=self.initial_data['external_num'],
            inbox=inbox,
            customer=customer,
            # object=unit,
            status=status
        )
        return contract

    def to_internal_value(self, data):
        res = super(ContractSer, self).to_internal_value(data)
        return res

class SelectChoicesSer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    value = serializers.CharField()


class SellSer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    value = serializers.CharField()


class RowSer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    sell = SellSer(many=True)


class HeaderSer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    type = serializers.CharField()
    align = serializers.CharField()
    sortable = serializers.BooleanField()
    editable = serializers.BooleanField()
    value = serializers.CharField()
    selectchoices = SelectChoicesSer(many=True, required=False)
    data = serializers.CharField(required=False)


class DocumentSer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class ReasonSer(serializers.Serializer):
    id = serializers.IntegerField()
    document = DocumentSer()
    point = serializers.CharField()
    phrasing = serializers.CharField()


class DefectSer(serializers.Serializer):
    id = serializers.IntegerField()
    reason = ReasonSer()
    phrasing = serializers.CharField()


class RowDefectsSer(serializers.Serializer):
    id = serializers.IntegerField()
    defect = DefectSer()

class TablesSer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    header = HeaderSer(many=True)
    row = RowSer(many=True)


class FormsSer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    table = TablesSer(many=True, required=False)


class ProtocolSer(serializers.ModelSerializer):
    form = FormsSer()

    class Meta:
        model = Protocol
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(ProtocolSer, self).__init__(*args, **kwargs)


class AllFormsSer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class SingleWorkRequestSer(serializers.Serializer):
    id = serializers.IntegerField()
    object = ObjectSer()


class WorkRequestSer(serializers.Serializer):
    id = serializers.IntegerField()
    form = FormsSer()
    contract = ContractSer()
    all_forms = AllFormsSer(many=True)
    objects = ObjectSer(many=True)


class ProtocolSer(serializers.Serializer):
    id = serializers.IntegerField()
    type_protocol = TypeProtocolSer()
    num = serializers.CharField()
    date_act = serializers.DateField()
    date_protocol = serializers.DateField()
    customer = OrganisationSer()
    owner = OrganisationSer()
    worker = UserAuthSer()
    device_set = DeviceSetSer()
    customer_person = UserAuthSer()
    owner_person = UserAuthSer()
    form = FormsSer()


class ObjRequestSer(serializers.ModelSerializer):
    object = ObjectSer()
    protocol = ProtocolSer(required=False)

    class Meta:
        model = ObjRequest
        fields = '__all__'


class WorkRequestListSer(serializers.ModelSerializer):
    contract = ContractSer()
    form = FormsSer()
    object_req = ObjRequestSer(many=True)

    class Meta:
        model = WorkRequest
        fields = '__all__'


class SellValueSer(serializers.Serializer):
    id = serializers.IntegerField()
    protocol = ProtocolSer()
    value = serializers.CharField()


class ObservedDefectSer(serializers.Serializer):
    id = serializers.IntegerField()
    sell_value = SellValueSer()
    defect = DefectSer()


class ProtocolAnnexSer(serializers.Serializer):
    id = serializers.IntegerField()
    sell_value = SellValueSer()
    type = serializers.CharField()
    name = serializers.CharField()
    file = serializers.FileField()


class RulesSer(serializers.Serializer):
    id = serializers.IntegerField()
    sell = SellSer()
    rule = serializers.CharField()


class FullSellSer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField()
    value = serializers.CharField()
    sell_value = SellValueSer(required=False)


class AnnexSer(serializers.Serializer):
    filename = serializers.FilePathField("./")
    filesize = serializers.SerializerMethodField('get_file_size')
    file = serializers.FileField()

    def get_file_size(self, obj):
        return "{} kb".format(obj.file.size/1000)


class FullRowSer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    sell = FullSellSer(many=True)


class FullTablesSer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    header = HeaderSer(many=True)
    dataset = serializers.ListField()
    collapse = serializers.BooleanField()
    defects = serializers.ListField()
    defects_header = serializers.ListField()
    annex_table = AnnexSer(many=True)


class FullProtocolSer(serializers.Serializer):
    tables = FullTablesSer(many=True)
    annex_table = AnnexSer(many=True)
    annex_table_headers = serializers.ListField()
    object = ObjectSer()


class FileFieldTestSer(serializers.Serializer):
    file = serializers.FileField()


class TableSer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    header = serializers.ListField()
    dataset = serializers.ListField()


class FormSer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField()
    tables = serializers.ListField(required=False)

    def create(self, validated_data):
        if 'id' in validated_data:
            form = Form.objects.get(id=validated_data['id'])
        else:
            form = Form.objects.create(name=validated_data['name'])
        for table in validated_data['tables']:
            t = Table.objects.get(id=table['id'])
            form.table_set.add(t)
        return form


class HeaderSerializer(serializers.ModelSerializer):
    selectchoices = SelectChoicesSer(source='selectchoices_set', many=True)

    class Meta:
        model = Header
        fields = [
            'id',
            'table',
            'text',
            'order',
            'align',
            'type',
            'sortable',
            'value',
            'width',
            'editable',
            'data',
            'selectchoices'
        ]
        queryset = Header.objects.order_by('order')


class SellSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sell
        fields = '__all__'


class RowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Row
        fields = '__all__'

    def to_representation(self, instance):
        sells = instance.sell_set.all()
        data = {'row_id': instance.id, 'row_order': instance.order, 'annex_table': []}
        for d in list(SellSerializer(sells, many=True).data):
            data[d['value']] = d['text']
        return data


class TableSerializer(serializers.ModelSerializer):
    header = HeaderSerializer(many=True, source='header_set')
    dataset = RowSerializer(source='row_set', many=True)
    annex_table = AnnexSer(source='protocolannex_set', many=True)
    defectheaders = serializers.ListField(default=[
        {
            "text": '№ п/п',
            "align": 'start',
            "sortable": False,
            "value": 'num',
            "width": '5%'
        },
        {"text": 'Наименование составных элементов электрооборудования лифта', "value": 'phrasing', "width": '30%'},
        {"text": 'Нормативная документация и перечень пунктов, устанавливающих требования', "value": 'document',
         "width": '30%'},
        {"text": '', "value": 'delete_action', "width": '5%'},
    ])
    collapse = serializers.BooleanField(default=True)
    expanded = serializers.ListField(default=[])

    class Meta:
        model = Table
        fields = ['id', 'name', 'header', 'dataset', 'annex_table', 'defectheaders', 'collapse', 'expanded']


    def to_representation(self, instance):
        data = super(TableSerializer, self).to_representation(instance)
        data['header'].sort(key=header_sort)
        data['dataset'].sort(key=row_sort)
        return data


class FormSerializer(serializers.ModelSerializer):
    tables = TableSerializer(many=True, source='table_set')

    class Meta:
        model = Form
        fields = ['id', 'name', 'tables']


class BankSerializer(serializers.Serializer):
    desc = serializers.CharField()
    bic = serializers.CharField()
    correspondent_account = serializers.CharField()
    inn = serializers.CharField()
    kpp = serializers.CharField()
    name = serializers.CharField()
    payment_account = serializers.CharField()


class CustomerSerializer(serializers.Serializer):
    desc = serializers.CharField()
    full_name = serializers.CharField()
    type_customer = serializers.CharField()
    head = serializers.CharField()
    head_name = serializers.CharField()
    head_lastname = serializers.CharField()
    head_surname = serializers.CharField()
    inn = serializers.CharField()
    kpp = serializers.CharField()
    ogrn = serializers.CharField()
    legal_address = serializers.CharField()
    post_address = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.CharField()
    contact_name = serializers.CharField()
    type_customer = serializers.CharField()


class ControlSerializer(serializers.Serializer):
    name = serializers.CharField()


class MethodSerializer(serializers.Serializer):
    name = serializers.CharField()


class ObjectSerializer(serializers.Serializer):
    name = serializers.CharField()


class Teable1RowSerializer(serializers.Serializer):
    address = serializers.CharField()
    object = serializers.CharField()
    element = serializers.CharField()
    count = serializers.CharField()


class TeableRowSerializer(serializers.Serializer):
    address = serializers.CharField()
    reg_num = serializers.CharField(source='reg_number')
    type_lift = serializers.CharField(source='type')
    capacity = serializers.CharField()
    floors = serializers.CharField()
    mf_year = serializers.CharField(source='manufactered')
    date_exam = serializers.CharField(source='last_verife')


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'


class NewLeadSerializer(serializers.ModelSerializer):
    bank = BankSerializer(required=False)
    customer = CustomerSerializer(required=False)
    controls = serializers.ListField(required=False)
    methods = serializers.ListField(required=False)
    objects = serializers.ListField(required=False)
    table_rows = TeableRowSerializer(many=True, required=False)
    table1_rows = Teable1RowSerializer(many=True, required=False)
    work = serializers.CharField(required=False)

    class Meta:
        model = Lead
        fields = ['id', 'bank', 'customer', 'controls', 'methods', 'objects', 'table1_rows', 'table_rows', 'work']


class AppSerializer(serializers.Serializer):
    app = serializers.CharField()


