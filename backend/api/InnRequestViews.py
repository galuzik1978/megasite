from rest_framework import authentication, permissions
from rest_framework.views import APIView

from api.serializers import get_organization_by_inn


class InnRequestView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get(request, format=None):
        inn = request.query_params['inn']
        return get_organization_by_inn(inn, request)

    @staticmethod
    def post(request, format=None):
        inn = request.query_params['inn']
        return get_organization_by_inn(inn, request)