from .models import Person, Watch
from rest_framework import serializers


class PersonSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=15, allow_null=False)
    age = serializers.IntegerField(max_value=255)
    etc = serializers.CharField(allow_null=False, max_length=100)

    class Meta:
        model = Person
        read_only_fields = ('create_at',)
        fields = "__all__"


class WatchSerializer(serializers.ModelSerializer):
    start_at = serializers.DateTimeField(required=True)
    end_at = serializers.DateTimeField(required=True)

    class Meta:
        model = Watch
        fields = "__all__"