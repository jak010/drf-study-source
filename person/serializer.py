import pytz

from .models import Person, Watch, BaseModel, PersonProfile
from rest_framework import serializers

from django.db import IntegrityError

from .exception import AlreadyExistPerson
from django.shortcuts import get_object_or_404


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


class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonProfile
        fields = ['description', 'level', 'person_id']

    def create(self, validated_data):
        try:
            return super(ProfileUpdateSerializer, self).create(validated_data)
        except IntegrityError as exc:
            if "Duplicate" in exc.args[1]:
                raise AlreadyExistPerson()

    def validate(self, attrs):
        person = get_object_or_404(Person, id=self.context['person_id'])

        # selected_related 사용법
        # select_related : OneToOneRel, Foreign Key
        # profile = PersonProfile.objects.select_related('person').get(person=person)

        attrs['person_id'] = person.id
        return attrs


class WatchSerializer(serializers.ModelSerializer):
    start_at = serializers.DateTimeField(required=True)
    end_at = serializers.DateTimeField(required=True)

    class Meta:
        model = Watch
        fields = "__all__"
