from django.contrib.auth.models import User
from rest_framework import authentication, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from api.interface import tables as all_tables

# Регистрируем все таблицы, доступные для конфигурирования (и последующей работы с ними из фронтенда)
from rest_framework.viewsets import ModelViewSet

from api.adminserializer import ModelSerializer
from develop.models import Division, Region, Machine
from mainWork.models import Status, TaskStatus, EventType, MainWork, Task, Message
from organisation.models import TypeOrganisation, ChoiceName, FormType, Element, Group, CityType, StreetType, TypeLift, \
    LiftDesign, TypeProtocol, DeviceSet, StatusDevice, TypeDevice, RangeMeasure, AccuracyClass, Organisation, Object, \
    Form, Protocol, Device, Document, Reason, DefectList, Table, Header, Row, Sell, SelectChoices, SellValue, \
    RowDefects, ObservedDefect, Rules, ProtocolAnnex, LeadStatus, LeadWork, Lead, LeadLog, WorkControl, WorkMethod, \
    WorkObjAddress, WorkObject, WorkType, WorkLift, WorkControlObject, LeadForm, FlawDetectionObject
from postoffice.models import TypeLetter, SendStatus, TypeWork, Inbox, Outbox, ContractStatus, Contract, WorkRequest, \
    ObjRequest
from user_profile.models import Role, Profile
from api.models import Table as AdminTable, Desk
from util import customize

all_models_list = [
    User,
    Division,
    Region,
    Machine,
    Role,
    Profile,
    TypeOrganisation,
    ChoiceName,
    FormType,
    Element,
    Group,
    CityType,
    StreetType,
    TypeLift,
    LiftDesign,
    TypeProtocol,
    DeviceSet,
    StatusDevice,
    TypeDevice,
    RangeMeasure,
    AccuracyClass,
    Organisation,
    Object,
    Form,
    Protocol,
    Device,
    Document,
    Reason,
    DefectList,
    Table,
    Header,
    Row,
    Sell,
    SelectChoices,
    SellValue,
    RowDefects,
    ObservedDefect,
    Rules,
    ProtocolAnnex,
    LeadStatus,
    LeadWork,
    Lead,
    LeadLog,
    WorkControl,
    WorkMethod,
    WorkObjAddress,
    WorkObject,
    WorkType,
    WorkLift,
    WorkControlObject,
    LeadForm,
    FlawDetectionObject,
    TypeLetter,
    SendStatus,
    TypeWork,
    Inbox,
    Outbox,
    ContractStatus,
    Contract,
    WorkRequest,
    ObjRequest,
    Status,
    TaskStatus,
    EventType,
    MainWork,
    Task,
    Message
]


class AppView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        models = [
            {
                'model':model._meta.model_name,
                'fields':[
                    field.name for field in model._meta.get_fields()
                ]
            } for model in all_models_list
        ]
        return Response(ModelSerializer(models, many=True).data)


class AdminTableView(ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = AdminTable.objects.all()


class CustomApiLoginView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        try:
            role_name = user.profile.role.name
        except Role.DoesNotExist:
            role_name = 'Должность не указана'

        # Заполняем данные рабочих таблиц и настроек рабочего стола, в зависимости от роли
        role = user.profile.role
        tables = AdminTable.objects.filter(role=role)
        if len(tables) == 0:
            role = Role.objects.get(name='Default')
            tables = AdminTable.objects.filter(role=role)
        data_tables = {
            all_tables[table.name].name:{
                'name': all_tables[table.name].name,
                'url': all_tables[table.name].url,
                'title': all_tables[table.name].title,
                'headers':[{
                    'text': header.text,
                    'align': header.align,
                    'sortable': header.sortable,
                    'value': header.value
                } for header in all_tables[table.name].headers],
                'edit': {
                    'title': all_tables[table.name].edit.title,
                    'fields': {
                        field.name:{
                            'type': field.type,
                            'name': field.name,
                            'text': getattr(field, 'text', None),
                            'width': getattr(field, 'width', None),
                            'icon': getattr(field, 'icon', None),
                            'value': getattr(field, 'value', None),
                            'subtable': getattr(field,'subtable', None)
                        } for field in all_tables[table.name].edit.fields
                    }
                },
            } for table in tables
        }
        for table in tables:
            if all_tables[table.name].filters:
                data_tables[table.name]['filters'] = [
                    {
                        'field': filter.field,
                        'value': filter.value
                    }
                    for filter in getattr(all_tables[table.name], 'filters', [])
                ]
            if all_tables[table.name].actions:
                data_tables[table.name]['actions'] = {
                    action.name: {
                        'text': action.text,
                        'color': action.color,
                        'icon': action.icon,
                        'url': action.url
                    } for action in all_tables[table.name].actions
                }
        desk = Desk.objects.filter(role=role)
        desk_config = {
            'sections':[
                {
                    'text': section.text,
                    'table': data_tables[section.table.get().name],
                    'icon': section.icon,
                    'color': section.color,
                    'router': section.router,
                    'is_active': section.is_active
                } if section.router else {
                    'text': section.text,
                    'table': data_tables[section.table.get().name],
                    'icon': section.icon,
                    'color': section.color,
                    'is_active': section.is_active
                }
                for section in desk],
            'start_page': desk.get(is_active=True).text
        }
        return Response({
            'token': token.key,
            'user': "{} {} {}".format(user.first_name, user.profile.surname, user.last_name),
            'role': role_name,
            'email': user.email,
            'desktop': desk_config['sections'],
            'tables': data_tables,
            'title': customize.TITLE,
            'logo': customize.LOGO,
            'company': customize.COMPANY,
            'start_page': desk.get(is_active=True).text
        })