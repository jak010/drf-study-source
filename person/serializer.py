from .models import Person
from rest_framework import serializers


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        read_only_fields = ('create_at',)
        fields = "__all__"

