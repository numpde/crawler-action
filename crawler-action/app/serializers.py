from rest_framework import serializers


class ContentSerializer(serializers.Serializer):
    url = serializers.URLField()
