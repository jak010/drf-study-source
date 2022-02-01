import pytz

from .models import Person, Watch, BaseModel
from rest_framework import serializers


# Refer
# - https://dev.to/juanbenitezdev/how-to-return-datetime-in-different-time-zones-from-django-rest-framework-1396
class BaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseModel
        fields = "__all__"
        abstract = True

    def to_representation(self, instance):
        self.fields['create_at'] = serializers.DateTimeField(default_timezone=pytz.timezone('Asia/Seoul'))
        self.fields['update_at'] = serializers.DateTimeField(default_timezone=pytz.timezone('Asia/Seoul'))
        return super().to_representation(instance)


class PersonSerializer(BaseSerializer):
    name = serializers.CharField(max_length=15, allow_null=False)
    age = serializers.IntegerField(max_value=255)
    etc = serializers.CharField(allow_null=False, max_length=100)

    class Meta:
        model = Person
        read_only_fields = ('create_at', 'update_at')
        fields = "__all__"


class WatchSerializer(serializers.ModelSerializer):
    start_at = serializers.DateTimeField(required=True)
    end_at = serializers.DateTimeField(required=True)

    class Meta:
        model = Watch
        fields = "__all__"
