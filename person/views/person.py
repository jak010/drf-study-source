from django.db import IntegrityError
import django_filters

from rest_framework.generics import ListCreateAPIView
from ..serializer import PersonSerializer
from ..exception import DuplicateNameError

from ..models import Person


class PersonFilter(django_filters.FilterSet):
    name = django_filters.AllValuesMultipleFilter()
    age = django_filters.NumberFilter(field_name='age', lookup_expr='exact')
    age_gt = django_filters.NumberFilter(field_name='age', lookup_expr='gte')
    age_lt = django_filters.NumberFilter(field_name='age', lookup_expr='lte')

    class Meta:
        model = Person
        fields = ['name', 'age']

    def __init__(self, *args, **kwargs):
        super(PersonFilter, self).__init__(*args, **kwargs)


class PersonListCreateAPIView(ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_class = PersonFilter

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise DuplicateNameError()
