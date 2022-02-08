import os
from datetime import datetime, date

import django
from django.contrib.auth.models import User
from django.core.files import File
from django.core.mail import EmailMessage, get_connection, send_mail
from django.http import JsonResponse, FileResponse
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from rest_framework import viewsets, permissions, authentication, status
from rest_framework.response import Response
from rest_framework.utils import json
from rest_framework.views import APIView

from api.word_utility import get_request_template, get_contract
from project_root import settings
from util import customize
from util.Mixins import FormMenuMixin

from api.serializers import InboxSer, SenderSer, ProfileSer, RoleSer, CustomerSer, TypeLetterSer, \
    SendStatusSer, TypeWorkSer, ContractSer, StatusSer, TaskStatusSer, EventTypeSer, MainWorkSer, TaskSer, MessageSer, \
    TypeCustomerSer, CityTypeSer, StreetTypeSer, TypeLiftSer, LiftDesignSer, TypeProtocolSer, DeviceSetSer, \
    StatusDeviceSer, TypeDeviceSer, RangeMeasureSer, AccuracyClassSer, ObjectSer, ProtocolSer, DeviceSer, \
    ManagerSer, OrganisationSer, FormsSer, TablesSer, HeaderSer, SellSer, RowSer, \
    SelectChoicesSer, WorkRequestSer, SellValueSer, RowDefectsSer, ReasonSer, DocumentSer, ObservedDefectSer, \
    ProtocolAnnexSer, RulesSer, ObjRequestSer, FullProtocolSer, FileFieldTestSer, AnnexSer, \
    TableSerializer, FormSerializer, LeadSerializer, UserSer, hint_address, get_dadata_bank, get_dadata
from organisation.models import Organisation, TypeOrganisation, CityType, StreetType, TypeLift, LiftDesign, \
    TypeProtocol, DeviceSet, \
    StatusDevice, TypeDevice, RangeMeasure, AccuracyClass, Object, Protocol, Device, Form, Table, Row, SellValue, \
    ProtocolAnnex, ObservedDefect, DefectList, Document, Header, Sell, Lead, LeadStatus, LeadForm, LeadWork, \
    WorkObject, FlawDetectionObject, WorkLift, WorkObjAddress, WorkControl
from mainWork.models import Status, TaskStatus, EventType, MainWork, Task, Message
from postoffice.models import Inbox, TypeLetter, SendStatus, TypeWork, Contract, WorkRequest, ObjRequest
from user_profile.models import Profile, Role
from util.customize import tables
from util.functions import capacity_text_to_decimal


class InnRequestView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get(request, format=None):
        inn = request.query_params['inn']
        return get_dadata(inn, request)

    @staticmethod
    def post(request, format=None):
        inn = request.query_params['inn']
        return get_dadata(inn, request)


class BankRequestView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get(request, format=None):
        bank = request.query_params['bank']
        return get_dadata_bank(bank, request)

    @staticmethod
    def post(request, format=None):
        bank = request.query_params['bank']
        return get_dadata_bank(bank, request)


class MainPageView(FormMenuMixin, TemplateView):
    template_name = "vue/index.html"


class SenderApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all().filter(is_staff=False)
    serializer_class = SenderSer


class UserApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all().filter(is_staff=True)
    serializer_class = UserSer


class ManagerApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all().filter(profile__role__name="Менеджер")
    serializer_class = ManagerSer


class ProfileApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSer


class RoleApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Role.objects.all()
    serializer_class = RoleSer


class CustomerApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Organisation.objects.all()
    serializer_class = CustomerSer


class OrganisationApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSer


class TypeLetterApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = TypeLetter.objects.all()
    serializer_class = TypeLetterSer


class SendStatusApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = SendStatus.objects.all()
    serializer_class = SendStatusSer


class TypeWorkApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = TypeWork.objects.all()
    serializer_class = TypeWorkSer


class ContractApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Contract.objects.all()
    serializer_class = ContractSer


class StatusApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Status.objects.all()
    serializer_class = StatusSer


class TaskStatusApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusSer


class EventTypeApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = EventType.objects.all()
    serializer_class = EventTypeSer


class MainWorkApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = MainWork.objects.all()
    serializer_class = MainWorkSer


class TaskApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSer


class MessageApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Message.objects.all()
    serializer_class = MessageSer


class TypeCustomerApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = TypeOrganisation.objects.all()
    serializer_class = TypeCustomerSer


class CityTypeApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = CityType.objects.all()
    serializer_class = CityTypeSer


class StreetTypeApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = StreetType.objects.all()
    serializer_class = StreetTypeSer


class TypeLiftApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = TypeLift.objects.all()
    serializer_class = TypeLiftSer


class LiftDesignApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = LiftDesign.objects.all()
    serializer_class = LiftDesignSer


class TypeProtocolApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = TypeProtocol.objects.all()
    serializer_class = TypeProtocolSer


class DeviceSetApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = DeviceSet.objects.all()
    serializer_class = DeviceSetSer


class StatusDeviceApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = StatusDevice.objects.all()
    serializer_class = StatusDeviceSer


class TypeDeviceApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = TypeDevice.objects.all()
    serializer_class = TypeDeviceSer


class RangeMeasureApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = RangeMeasure.objects.all()
    serializer_class = RangeMeasureSer


class AccuracyClassApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = AccuracyClass.objects.all()
    serializer_class = AccuracyClassSer


class ObjectApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Object.objects.all()
    serializer_class = ObjectSer


class ProtocolApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Protocol.objects.all()
    serializer_class = ProtocolSer

    def retrieve(self, request, *args, **kwargs):
        exam_object = ObjRequest.objects.get(**kwargs)
        protocol = exam_object.protocol
        if protocol is None:
            # Создаем новый протокол
            protocol = Protocol.objects.create(
                form=exam_object.work_request.form
            )
            exam_object.protocol = protocol
            exam_object.save()
        data = protocol.form
        data.object = exam_object.object
        data.tables = data.table_set.all()
        protocol_annex = protocol.protocolannex_set.filter(table_id__isnull=True)
        data.annex_table = protocol_annex
        data.annex_table_headers = [
            {
                'text': "№ п/п",
                'value': 'num',
                'width': '5%',
            },
            {
                'text': "Изображение",
                'value': 'img',
                'width': '30%',
            },
            {
                'text': "Имя файла",
                'value': 'filename',
                'width': '30%',
            },
            {
                'text': "Размер файла",
                'value': 'filesize',
                'width': '20%',
            },
            {
                'text': "Удалить",
                'value': 'actions',
                'width': '15%',
            },
        ]
        for table in data.tables:
            table.header = table.header_set.all().order_by('id')
            for header in table.header:
                header.selectchoices = header.selectchoices_set.all()
            table.defects_header = [
                {
                    "text": '№ п/п',
                    "align": 'start',
                    "sortable": False,
                    "value": 'num',
                    "width": '5%'
                },
                {"text": 'Наименование составных элементов электрооборудования лифта', "value": 'phrasing',
                 "width": '30%'},
                {"text": 'Нормативная документация и перечень пунктов, устанавливающих требования', "value": 'document',
                 "width": '30%'},
                {"text": '', "value": 'delete_action', "width": '5%'},
            ]
            table.annex_table = protocol.protocolannex_set.filter(table_id=table).filter(row_id__isnull=True)
            table.defects = []
            for defect in table.rowdefects_set.all():
                table.defects.append(
                    {
                        'document': defect.defect.reason.document.name,
                        'phrasing': defect.defect.phrasing
                    }
                )
            rows = table.row_set.all()
            table.dataset = []
            for num, row in enumerate(rows):
                dataset = {
                    'num': num + 1,
                    'id': row.id,
                    'annex_table': AnnexSer(
                        protocol.protocolannex_set.filter(row_id=row),
                        many=True
                    ).data,
                    'defects': []
                }
                sells = row.sell_set.all()
                for sell in sells:
                    sell.sell_value = sell.sellvalue_set.filter(protocol=protocol).first()
                    if sell.sell_value is None:
                        dataset[sell.value] = sell.text
                    else:
                        dataset[sell.value] = sell.sell_value.value
                        for defect in sell.sell_value.observeddefect_set.all():
                            dataset['defects'].append({
                                'document': defect.defect.reason.document.name,
                                'phrasing': defect.defect.phrasing
                            })

                table.dataset.append(dataset)
                table.collapse = True
        return Response(FullProtocolSer(data).data)

    def update(self, request, *args, **kwargs):
        data = json.loads(request.data['data'])

        # Получим экземпляр обновляемого протокола из базы данных
        exam_object = ObjRequest.objects.get(**kwargs)
        protocol = exam_object.protocol

        # Обновим приложения, привязанные непосредственно к протоколу

        # Удаляем приложения, отсутствующие во вновь получнных данных
        annex_filenames = [annex['filename'] for annex in data['annex_table']]
        for annex in protocol.protocolannex_set.filter(table__isnull=True):
            if (annex.filename in annex_filenames) == False:
                annex.delete()

        # Добавим новые приложения, отсутствующие в базе
        for annex in data['annex_table']:
            if len(protocol.protocolannex_set.filter(filename=annex['filename'])) == 0:
                ProtocolAnnex.objects.create(
                    protocol=protocol,
                    filename=annex['filename'],
                    file=request.FILES['file_{}'.format(annex['img'])],
                )

        # Заполним SellValue получеными данными
        for t in data['tables']:
            table = Table.objects.get(pk=t['id'])
            # Удаляем приложения, отсутствующие во вновь получнных данных
            annex_filenames = [annex['filename'] for annex in t['annex_table']]
            for annex in protocol.protocolannex_set.filter(table=table).filter(row__isnull=True):
                if (annex.filename in annex_filenames) == False:
                    annex.delete()

            for annex in t['annex_table']:
                if len(protocol.protocolannex_set.filter(table=table).filter(filename=annex['filename'])) == 0:
                    ProtocolAnnex.objects.create(
                        protocol=protocol,
                        table=table,
                        filename=annex['filename'],
                        file=request.FILES['file_{}'.format(annex['img'])],
                    )
            # Выбиаем из заголовков только те поля, в которых задано значение data
            headers = table.header_set.filter(data__isnull=False)
            for r in t['dataset']:
                row = Row.objects.get(pk=r['id'])
                # Удаляем приложения, отсутствующие во вновь получнных данных
                annex_filenames = [annex['filename'] for annex in r['annex_table']]
                for annex in protocol.protocolannex_set.filter(table=table).filter(row=row):
                    if (annex.filename in annex_filenames) == False:
                        annex.delete()
                for annex in r['annex_table']:
                    if len(protocol.protocolannex_set.filter(table=table).filter(row=row).filter(
                            filename=annex['filename'])) == 0:
                        ProtocolAnnex.objects.create(
                            protocol=protocol,
                            table=table,
                            row=row,
                            filename=annex['filename'],
                            file=request.FILES['file_{}'.format(annex['img'])],
                        )
                # Вибираем ячейки, совпадающие с именем в заголовке
                for header in headers:
                    print(header.data)
                    sell = row.sell_set.get(value=header.data)
                    try:
                        sell_value = sell.sellvalue_set.get(protocol=protocol)
                        sell_value.value = r[header.data]
                        sell_value.save()
                    except  SellValue.DoesNotExist as err:
                        sell_value = SellValue.objects.create(sell=sell, protocol=protocol, value=r[header.data])
                    except django.db.utils.IntegrityError as err:
                        pass
                    # Удаляем дефекты, отсутствующие в полученных данных из базы
                    old_defects = sell_value.observeddefect_set.all()
                    for old in old_defects:
                        if ({'document': old.defect.reason.document.name, 'phrasing': old.defect.phrasing} in r[
                            'defects']) == False:
                            old.delete()

                    # Добавляем новые дефекты, отсутствующие в базе
                    try:
                        for defect in r['defects']:
                            # Находим отмеченный дефект в базе
                            doc = Document.objects.filter(name=defect['document']).first()
                            reason_phrase = defect['phrasing'].split(":")[1].strip()
                            reason = doc.reason_set.get(phrasing=reason_phrase)
                            new_defect = DefectList.objects.filter(reason=reason).get(phrasing=defect['phrasing'])
                            if len(old_defects.filter(defect=new_defect)) == 0:
                                ObservedDefect.objects.create(
                                    sell_value=sell_value,
                                    defect=new_defect
                                )
                    except KeyError:
                        pass

        response_status = status.HTTP_200_OK
        return Response("Данные успешно обновлены", status=response_status)


class DeviceApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Device.objects.all()
    serializer_class = DeviceSer


class TemplateView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request, format=None):
        return Response({'desktop': customize.desk_config, 'tables': customize.tables})

    @staticmethod
    def post(request, format=None):
        return Response({'desktop': customize.desk_config, 'tables': customize.tables})


class CreateContractByInboxView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        inbox = Inbox.objects.get(pk=kwargs['inbox'])
        table = tables['contract']
        table['edit']['fields']['inbox']['value'] = InboxSer(inbox).data
        table['edit']['fields']['customer']['value'] = CustomerSer(inbox.customer).data
        table['edit']['fields']['type_work']['value'] = TypeWorkSer(inbox.type_work).data
        return JsonResponse(table)


class GetBlankView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def post(request, *args, **kwargs):
        f = FileResponse(open("../Основные функции.ods", 'rb'))
        return f

    @staticmethod
    def get(request, *args, **kwargs):
        return FileResponse("Основные функции.ods")


class FormsView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get(request, format=None):
        forms = Form.objects.all()
        response = []
        for form in Form.objects.all():
            form.table = []
            for table in form.table_set.all():
                table.header = []
                for header in table.header_set.all():
                    query = header.selectchoices_set.all()
                    if len(query):
                        header.selectchoices = []
                        for selectchoice in query:
                            header.selectchoices.append(SelectChoicesSer(selectchoice).data)
                    table.header.append(HeaderSer(header).data)
                table.row = []
                for row in table.row_set.all():
                    row.sell = []
                    for sell in row.sell_set.all():
                        sell.sell_value = []
                        for sell_value in sell.sellvalue_set.all():
                            sell_value.observed_defect = []
                            for observed_defect in sell_value.observeddefect_set.all():
                                sell_value.observed_defect.append(ObservedDefectSer(observed_defect).data)
                            sell_value.annex = []
                            for annex in sell_value.protocolannex_set.all():
                                sell_value.annex.append(ProtocolAnnexSer(annex).data)
                            sell.sell_value.append((SellValueSer(sell_value).data))
                        sell.rules = []
                        for rules in sell.rules_set.all():
                            sell.rules.append(RulesSer(rules).data)
                        row.sell.append(SellSer(sell).data)
                    row.rowdefect = []
                    for row_defects in row.rowdefects_set.all():
                        row_defects.reason = []
                        for reason in row_defects.reason_set.all():
                            reason.document = []
                            for document in reason.document_set.all():
                                reason.document.append((DocumentSer(document).data))
                            row_defects.reason.append(ReasonSer(reason).data)
                        row.rowdefect.append(RowDefectsSer(row_defects).data)
                    table.row.append(RowSer(row).data)
                form.table.append(TablesSer(table).data)
            response.append({'form': FormsSer(form).data})
        return Response(response)

    @staticmethod
    def post(request, format=None):
        return Response({'desktop': customize.desk_config, 'tables': customize.tables})


class NewWorkRequestView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        contract = Contract.objects.get(pk=kwargs['contract'])
        work_request = WorkRequest(contract=contract)
        work_request.save()
        serializer = WorkRequestSer(work_request)
        response_status = status.HTTP_200_OK
        return Response(serializer.data, status=response_status)

    @staticmethod
    def get(request, *args, **kwargs):
        contract = Contract.objects.get(pk=kwargs['contract'])
        try:
            work_request = contract.workrequest_set.get()
        except WorkRequest.DoesNotExist as err:
            work_request = WorkRequest(contract=contract)
            work_request.save()
        serializer = WorkRequestSer(work_request)
        response_status = status.HTTP_200_OK
        return Response(serializer.data, status=response_status)


class WorkRequestView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def post(request, *args, **kwargs):
        """
        Сохранение/обновление заявок на проведение работ, а также контракта,
        связанного с этими заявками.
        """
        contract = Contract.objects.get(pk=kwargs['contract'])
        # Обновляем данные заказчика в соответствии с заявкой
        contract.customer.inn = int(request.data['inn']) if request.data['inn'] != 'null' else None
        contract.customer.full_name = request.data['full_name']
        contract.customer.head = request.data['head']
        contract.customer.head_last_name = request.data['head_last_name']
        contract.customer.head_name = request.data['head_name']
        contract.customer.head_surname = request.data['head_surname']
        contract.customer.ogrn = int(request.data['ogrn']) if request.data['ogrn'] != 'null' else None
        contract.customer.kpp = int(request.data['kpp']) if request.data['kpp'] != 'null' else None
        contract.customer.legal_address = request.data['address']
        contract.customer.post_address = request.data['post_address']
        contract.customer.bic = int(request.data['bik']) if request.data['bik'] != 'null' else None
        contract.customer.bank = request.data['bank']
        contract.customer.account = int(request.data['account']) if request.data['account'] != 'null' else None
        contract.customer.cor_account = int(request.data['korr_account']) if request.data[
                                                                                 'korr_account'] != 'null' else None
        try:
            contract.customer.type_customer = TypeOrganisation.objects.get(name=request.data['type_customer'])
        except TypeOrganisation.DoesNotExist:
            type_customer = TypeOrganisation(name=request.data['type_customer'])
            type_customer.save()
            contract.customer.type_customer = type_customer
        contract.customer.save()
        new_form = json.loads(request.data['form'])
        try:
            form = Form.objects.get(pk=new_form['id'])
        except TypeError:
            form = None
        table_rows = json.loads(request.data['table_rows'])
        try:
            work_request = contract.workrequest_set.get()
        except WorkRequest.DoesNotExist:
            work_request = WorkRequest(contract=contract, form=form)
            work_request.save()
        # Удаляем заявки текущего договора, отсутствующие в полученном запросе, но присутствующие в базе
        objects_id = [row.get('id') for row in table_rows]
        for work_object in work_request.object_req.all():
            if work_object.id not in objects_id:
                work_object.delete()
        for obj in table_rows:
            obj['address'] = obj['address']
            # расифровываем адрес через Dadata.ru
            address = hint_address(obj['address'], request).data
            try:
                city_type = CityType.objects.get(name=address['city_type'])
            except CityType.DoesNotExist:
                city_type = CityType(name=address['city_type'])
                city_type.save()
            try:
                street_type = StreetType.objects.get(name=address['street_type'])
            except StreetType.DoesNotExist:
                street_type = StreetType(name=address['street_type'])
                street_type.save()
            try:
                type_lift = TypeLift.objects.get(name=obj['type_lift']['name'])
            except TypeLift.DoesNotExist:
                type_lift = TypeLift(name=obj['type_lift']['name'])
                type_lift.save()
            if obj.get('id', False):
                # Если заявка уже зарегистрирована
                work_object = work_request.object_req.get(pk=obj['id'])
                work_object.postcode = int(address['postcode']) if address['postcode'] != 'null' else None
                work_object.region = address['region']
                work_object.city = address['city']
                work_object.street_type = street_type
                work_object.city_type = city_type
                work_object.street = address['street']
                work_object.building = address['building']
                work_object.reg_num = obj['reg_num']
                work_object.mf_year = datetime.strptime(obj['mf_year'], '%Y')
                work_object.type_lift = type_lift
                work_object.capacity = capacity_text_to_decimal(obj['capacity'])
                work_object.floors = int(obj['floors']) if obj['floors'] != 'null' else None
                work_object.date_exam = datetime.strptime(obj['date_exam'], '%Y-%m').date()
                work_object.save()
            else:
                work_object = Object(
                    postcode=int(address['postcode']) if address['postcode'] else None,
                    region=address['region'],
                    city_type=city_type,
                    city=address['city'],
                    street_type=street_type,
                    street=address['street'],
                    building=address['building'],
                    reg_num=obj['reg_num'],
                    mf_year=datetime.strptime(obj['mf_year'], '%Y'),
                    type_lift=type_lift,
                    capacity=capacity_text_to_decimal(obj['capacity']),
                    floors=int(obj['floors']) if obj['floors'] != 'null' else None,
                    date_exam=datetime.strptime(obj['date_exam'], '%Y-%m').date(),
                )
                work_object.save()
                work_request.object_req.add(work_object)

        work_request.form = form
        work_request.save()
        response_status = status.HTTP_200_OK
        return Response("", status=response_status)

    @staticmethod
    def get(request, *args, **kwargs):
        """
        Выдача данных по заявкам на провдение работ и связанным сущностям
        """
        contract = Contract.objects.get(pk=kwargs['contract'])
        try:
            work_request = contract.workrequest_set.get()
        except WorkRequest.DoesNotExist as err:
            work_request = WorkRequest(contract=contract)
            work_request.save()
        work_request.all_forms = Form.objects.all()
        data = {
            'id': kwargs['contract'],
            'form': work_request.form,
            'contract': contract,
            'all_forms': Form.objects.all(),
            'objects': work_request.object_req.all()
        }
        serializer = WorkRequestSer(data)
        response_status = status.HTTP_200_OK
        return Response(serializer.data, status=response_status)


class WorkRequestListView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        data = {
            'work_requests': WorkRequest.objects.all()
        }
        obj = ObjRequest.objects.all()
        res = ObjRequestSer(obj, many=True)
        return Response(res.data)


class FileFieldTestView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        inboxes = Inbox.objects.all()
        files = []
        for inbox in inboxes:
            if inbox.annex.name:
                files.append({'file': inbox.annex})
        res = FileFieldTestSer(files, many=True)
        return Response(res.data)


class TableApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    def create(self, request, *args, **kwargs):
        try:
            table = Table.objects.get(pk=request.data['id'])
            table.name = request.data['name']
            table.save()
        except Table.DoesNotExist:
            table = Table.objects.create(
                name=request.data['name']
            )
        # Удаляем заголовки из базы данных, отсутствующие в принятом массиве
        headers = Header.objects.filter(table=table)
        ids = [h['id'] for h in request.data['header']]
        for header in headers:
            if header.id not in ids:
                header.delete()

        for header in request.data['header']:
            try:
                h = Header.objects.get(pk=header['id'])
                h.table = table
                h.text = header['text']
                h.order = header['order']
                h.align = header['align']
                h.type = header['type']
                h.sortable = header['sortable']
                h.value = header['value']
                h.width = header['width']
                h.editable = header['editable']
                h.data = header['data']
                h.save()
            except Header.DoesNotExist:
                h = Header.objects.create(
                    table=table,
                    text=header['text'],
                    order=header['order'],
                    align=header['align'],
                    type=header['type'],
                    sortable=header['sortable'],
                    value=header['value'],
                    width=header['width'],
                    editable=header['editable'],
                    data=header['data']
                )
        # Удаляем ряды, отсутствующие в принятых данных
        rows = Row.objects.filter(table=table)
        ids = [row['row_id'] for row in request.data['dataset']]
        for row in rows:
            if row.id not in ids:
                sells = Sell.objects.filter(row=row)
                for sell in sells:
                    sell.delete()
                row.delete()

        for row in request.data['dataset']:
            try:
                r = Row.objects.get(pk=row['row_id'])
                r.table = table
                r.order = row['row_order']
                r.name = row['name']
                r.save()
            except Row.DoesNotExist:
                r = Row.objects.create(
                    table=table,
                    order=row['row_order'],
                    name=row['name']
                )
            row_sells = Sell.objects.filter(row=r)
            for col in row:
                try:
                    s = row_sells.get(value=col)
                    s.row = r
                    s.text = row[col]
                    s.value = col
                    s.save()
                except Sell.DoesNotExist:
                    s = Sell.objects.create(
                        row=r,
                        text=row[col],
                        value=col
                    )
        response_status = status.HTTP_200_OK
        return Response("Все океюшки", status=response_status)

    def update(self, request, *args, **kwargs):
        return super(TableApiView, self).update(request, *args, **kwargs)


class FormApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    queryset = Form.objects.all()
    serializer_class = FormSerializer


class LeadApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    @staticmethod
    def send_request(lead:Lead):
        html_content = render_to_string('mail/request_mail.html', {'UUID': lead.uuid})
        mail = EmailMessage(
            to=[lead.customer_email],
            subject='Ваша заявка получена',
            body=html_content
        )
        mail.attach_file(lead.lead_form.first().form.path)
        mail.content_subtype = 'html'
        mail.send(fail_silently=False)

    def create(self, request, *args, **kwargs):
        data = request.data
        file_name = get_request_template(data)

        try:
            lead_status = LeadStatus.objects.get(name="необработанная заявка")
        except LeadStatus.DoesNotExist:
            lead_status = LeadStatus.objects.create(name="необработанная заявка")

        try:
            lead_work = LeadWork.objects.get(name=data.get('work'))
        except LeadWork.DoesNotExist:
            lead_work = LeadWork.objects.create(name=data.get('work'))

        try:
            customer_type = TypeOrganisation.objects.get(name=data['customer'].get('type_customer'))
        except TypeOrganisation.DoesNotExist:
            customer_type = TypeOrganisation.objects.create(name=data['customer'].get('type_customer'))

        lead = Lead.objects.create(
            customer_full_name=data['customer'].get('full_name'),
            customer_type=customer_type,
            customer_head=data['customer'].get('head'),
            customer_name=data['customer'].get('head_name'),
            customer_surname=data['customer'].get('head_surname'),
            customer_lastname=data['customer'].get('head_lastname'),
            customer_inn=data['customer'].get('inn'),
            customer_kpp=data['customer'].get('kpp'),
            customer_ogrn=data['customer'].get('ogrn'),
            customer_contact_name=data['customer'].get('contact_name'),
            customer_email=data['customer'].get('email'),
            customer_phone=data['customer'].get('phone'),
            customer_legal_address=data['customer'].get('legal_address'),
            customer_post_address=data['customer'].get('post_address'),
            bank_name=data['bank'].get('name'),
            bank_bic=data['bank'].get('bic'),
            bank_inn=data['bank'].get('inn'),
            bank_kpp=data['bank'].get('kpp'),
            bank_correspondent_account=data['bank'].get('correspondent_account'),
            bank_payment_account=data['bank'].get('payment_account'),
            work=lead_work,
            status=lead_status
        )
        if request.user.is_staff:
            try:
                lead_status = LeadStatus.objects.get(name="проверенная заявка")
            except LeadStatus.DoesNotExist:
                lead_status = LeadStatus.objects.create(name="проверенная заявка")
            lead.status = lead_status

            try:
                customer = Organisation.objects.get(inn=data['customer']['inn'])
            except Organisation.DoesNotExist:
                customer = Organisation.objects.create(
                    inn=data['customer']['inn'], type_customer=customer_type
                )
        lead_form = LeadForm.objects.create(
            lead=lead,
            name=file_name,
            form=File(open(file_name, 'rb')),
        )

        if 'неразрушающего контроля' in lead.work.name:
            for obj in data['objects']:
                work_object = WorkObject.objects.create(
                    lead=lead,
                    # address=obj
                )
            for method in data['methods']:
                work_method = WorkObject.objects.create(
                    lead=lead,
                    name=method
                )
            for row in data['table1_rows']:
                FlawDetectionObject.objects.create(
                    address=row['address'],
                    object=row['object'],
                    element=row['element'],
                    count=int(row['count']),
                    lead=lead
                )
        elif 'оценки соответствия лифта' in lead.work.name:
            for row in data['table_rows']:
                tmp = row['date_exam'].split('-')
                tmp.append('1')
                s = [int(r) for r in tmp]
                last_verife = date(s[0], s[1], s[2])
                WorkLift.objects.create(
                    address=row['address'],
                    reg_number=row['reg_num'],
                    type=row['type_lift'],
                    capacity=row['capacity'],
                    floors=int(row['floors']),
                    manufactured=int(row['mf_year']),
                    last_verife=last_verife,
                    lead=lead
                )
        elif 'испытаний электрооборудования' in lead.work.name:
            WorkObjAddress.objects.create(
                address=data['obj_address'],
                lead=lead
            )
            for control in data['controls']:
                WorkControl.objects.create(
                    name=control,
                    lead=lead
                )
        else:
            response_status = status.HTTP_404_NOT_FOUND
            return Response("Неизвестный вид работы", status=response_status)
        LeadApiView.send_request(lead)
        # customer = models.ForeignKey(Organisation, on_delete=models.PROTECT)
        response_status = status.HTTP_200_OK
        return FileResponse(lead_form.form, status=response_status)


class SendRequestView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request, lead):
        lead = Lead.objects.get(pk=lead)
        LeadApiView.send_request(lead)
        response_status = status.HTTP_200_OK
        return Response("Заявка отправлена заказчику", status=response_status)


class SendContractView(APIView):
    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.AllowAny]

    def post(self, request, lead):
        lead = Lead.objects.get(pk=lead)
        get_contract(lead)
        response_status = status.HTTP_200_OK
        return Response("Договор отправлен заказчику", status=response_status)
