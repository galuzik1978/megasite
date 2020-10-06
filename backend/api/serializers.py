import json

import requests
from django.contrib.auth.models import User
from django.db.models import Max
from django.utils.datetime_safe import datetime
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status
from rest_framework.fields import empty
from rest_framework.response import Response

from organisation.models import Organisation, TypeOrganisation, CityType, StreetType, TypeLift, LiftDesign, \
    TypeProtocol, DeviceSet, StatusDevice, TypeDevice, RangeMeasure, AccuracyClass, Object, Protocol, Device
from mainWork.models import Status, TaskStatus, EventType, MainWork, Task, Message
from postoffice.models import Inbox, Outbox, TypeLetter, SendStatus, TypeWork, Contract
from user_profile.models import Profile, Role
from util.customize import Company_INN, Company_Phone

token = 'e01d0b0411274cc94fd22aa9c2bf5bf5d9f14936' # "Replace with Dadata API key"
secret = '29a8f7d7d8528121a4ecdeddc9796dc68d1c40f5' # "Replace with Dadata secret key"


class TypeCustomerSer(serializers.ModelSerializer):
    class Meta:
        model = TypeOrganisation
        fields = '__all__'


def get_organization_by_inn(inn, request):
    url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/party"
    headers={
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
        except TypeOrganisation.DoesNotExist as e:
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
                'type_customer': TypeCustomerSer(type_customer, context={'request': request}).data
            }
        else:
            raise Exception("Не известная форма собственности: {}".format(res['type']))
        response_status = status.HTTP_200_OK
        data['len'] = len(r.json()['suggestions'])
    except IndexError as e:
        data = "Проверьте ИНН. ИНН не найден в базе"
        response_status = status.HTTP_404_NOT_FOUND

    return Response(data, status=response_status)


class RoleSer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class ProfileSer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(ProfileSer, self).__init__(*args, **kwargs)

    def validate_user(self, value):
        return value


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
            'last_name': self.initial_data['name'],
            'email': self.initial_data['email'],
        }
        role_pk = json.loads(self.initial_data['role'])['id']
        role = Role.objects.get(pk=role_pk)
        customer_pk = json.loads(self.initial_data['customer'])['id']
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


class CustomerSer(serializers.ModelSerializer):
    type_customer = MyTypeCustomerSer()

    class Meta:
        model = Organisation
        fields = [
            'id', 'inn', 'inn_filial', 'full_name', 'type_customer', 'head',
            'head_name', 'head_surname', 'head_last_name', 'kpp', 'ogrn',
            'phone', 'add_phone', 'fax'
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

class OrganisationSer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(OrganisationSer, self).__init__(*args, **kwargs)


class SendStatusSer(serializers.ModelSerializer):
    class Meta:
        model = SendStatus
        fields = ['id', 'name']


class TypeWorkSer(serializers.ModelSerializer):
    class Meta:
        model = TypeWork
        fields = '__all__'


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


class ContractSer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(ContractSer, self).__init__(*args, **kwargs)


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
    class Meta:
        model = Object
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(ObjectSer, self).__init__(*args, **kwargs)


class ProtocolSer(serializers.ModelSerializer):
    class Meta:
        model = Protocol
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        kwargs['partial'] = True
        super(ProtocolSer, self).__init__(*args, **kwargs)


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
