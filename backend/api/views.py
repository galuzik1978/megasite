from django.contrib.auth.models import User
import requests
from django.views.generic import TemplateView
from rest_framework import viewsets, permissions, authentication, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from util import customize
from util.Mixins import FormMenuMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from api.serializers import InboxSer, OutboxSer, SenderSer, ProfileSer, RoleSer, CustomerSer, TypeLetterSer, \
    SendStatusSer, TypeWorkSer, ContractSer, StatusSer, TaskStatusSer, EventTypeSer, MainWorkSer, TaskSer, MessageSer, \
    TypeCustomerSer, CityTypeSer, StreetTypeSer, TypeLiftSer, LiftDesignSer, TypeProtocolSer, DeviceSetSer, \
    StatusDeviceSer, TypeDeviceSer, RangeMeasureSer, AccuracyClassSer, ObjectSer, ProtocolSer, DeviceSer
from organisation.models import Organisation, TypeOrganisation, CityType, StreetType, TypeLift, LiftDesign, \
    TypeProtocol, DeviceSet, \
    StatusDevice, TypeDevice, RangeMeasure, AccuracyClass, Object, Protocol, Device
from mainWork.models import Status, TaskStatus, EventType, MainWork, Task, Message
from postoffice.models import Inbox, Outbox, TypeLetter, SendStatus, TypeWork, Contract
from user_profile.models import Profile, Role

token = 'e01d0b0411274cc94fd22aa9c2bf5bf5d9f14936' # "Replace with Dadata API key"
secret = '29a8f7d7d8528121a4ecdeddc9796dc68d1c40f5' # "Replace with Dadata secret key"


class MainPageView(FormMenuMixin, TemplateView):
    template_name = "vue/index.html"


class InboxApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Inbox.objects.all().order_by('date')
    serializer_class = InboxSer


class OutboxApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Outbox.objects.all().order_by('date')
    serializer_class = OutboxSer


class SenderApiView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = SenderSer


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
    # authentication_classes = [authentication.TokenAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
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


class CustomApiLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': "{} {} {}".format(user.first_name, user.profile.surname, user.last_name),
            'role': user.profile.role.name,
            'email': user.email,
            'desktop': customize.desk_config['manager']['sections'],
            'tables': customize.tables,
            'title': customize.TITLE,
            'logo': customize.LOGO,
            'company': customize.COMPANY
        })


class InnRequestView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request, format=None):
        inn = request.query_params['inn']
        return get_organization_by_inn(inn, request)

    @staticmethod
    def post(request, format=None):
        inn = request.query_params['inn']
        return get_organization_by_inn(inn, request)


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
    except IndexError as e:
        data = "Проверьте ИНН. ИНН не найден в базе"
        response_status = status.HTTP_404_NOT_FOUND
    data['len'] = len(r.json()['suggestions'])
    return Response(data, status=response_status)
