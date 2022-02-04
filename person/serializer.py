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


class PersonSerializer(BaseSerializer):
    name = serializers.CharField(max_length=15, allow_null=False)
    age = serializers.IntegerField(max_value=255)

    class Meta:
        model = Person
        read_only_fields = ('create_at', 'update_at')
        fields = "__all__"

    def to_representation(self, instance):
        self.fields['create_at'] = serializers.DateTimeField(default_timezone=pytz.timezone('Asia/Seoul'))
        self.fields['update_at'] = serializers.DateTimeField(default_timezone=pytz.timezone('Asia/Seoul'))
        return super().to_representation(instance)


class PersonUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=15, required=False)
    age = serializers.IntegerField(max_value=255, required=False)
    etc = serializers.CharField(max_length=255, required=False)

    class Meta:
        model = Person
        fields = ['name', 'age', 'etc']


class WatchSerializer(serializers.ModelSerializer):
    start_at = serializers.DateTimeField(required=True)
    end_at = serializers.DateTimeField(required=True)

    class Meta:
        model = Watch
        fields = "__all__"
