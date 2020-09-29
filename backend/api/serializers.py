from django.contrib.auth.models import User
from django.db.models import Max
from django.utils.datetime_safe import datetime
from rest_framework import serializers
from rest_framework.fields import empty

from organisation.models import Organisation, TypeOrganisation, CityType, StreetType, TypeLift, LiftDesign, \
    TypeProtocol, DeviceSet, StatusDevice, TypeDevice, RangeMeasure, AccuracyClass, Object, Protocol, Device
from mainWork.models import Status, TaskStatus, EventType, MainWork, Task, Message
from postoffice.models import Inbox, Outbox, TypeLetter, SendStatus, TypeWork, Contract
from user_profile.models import Profile, Role


class RoleSer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class ProfileSer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

    def validate_user(self, value):
        return value


class SenderSer(serializers.ModelSerializer):
    profile = ProfileSer(required=False)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'profile']

    def create(self, validated_data):
        user_data = {
            'username': self.initial_data['email'],
            'first_name': self.initial_data['first_name'],
            'last_name': self.initial_data['name'],
            'email': self.initial_data['email'],
        }
        role = Role.objects.filter(pk=self.initial_data['role'])[0]
        customer = Organisation.objects.filter(pk=self.initial_data['customer'])[0]
        user = User(** user_data)
        user.save()
        user.profile.surname = self.initial_data['profile.surname']
        user.profile.phone = self.initial_data['profile.phone']
        user.profile.organisation = customer
        user.profile.role = role
        user.save()
        return user


class CustomerSer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = '__all__'


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

    def create(self, validated_data):
        sender = User.objects.get(pk=self.initial_data['sender'])
        try:
            num = Inbox.objects.all().aggregate(Max('num')) + 1
        except TypeError as err:
            num = 1
        customer = sender.profile.organisation
        send_status = SendStatus.objects.get(pk=self.initial_data['send_status'])
        type_work = TypeWork.objects.get(pk=self.initial_data['type_work'])
        try:
            type_letter = TypeLetter.objects.get(name="Новая заявка")
        except TypeLetter.DoesNotExist as err:
            type_letter = TypeLetter.objects.create(name="Новая заявка")
        annex = validated_data['annex']
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


class ContractSer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'


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


class TaskSer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class MessageSer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class TypeCustomerSer(serializers.ModelSerializer):
    class Meta:
        model = TypeOrganisation
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


class ProtocolSer(serializers.ModelSerializer):
    class Meta:
        model = Protocol
        fields = '__all__'


class DeviceSer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class UserAuthSer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

