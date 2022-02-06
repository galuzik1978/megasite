from rest_framework import serializers
from api.models import Table as AdminTable


class ModelSerializer(serializers.Serializer):
    model = serializers.CharField(read_only=True)
    fields = serializers.ListField(read_only=True)

