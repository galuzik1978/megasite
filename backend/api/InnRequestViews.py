from rest_framework import authentication, permissions
from rest_framework.views import APIView

from api.serializers import get_organization_by_inn, get_dadata, get_dadata_bank


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