from django.db import IntegrityError
import django_filters

from rest_framework.generics import ListCreateAPIView
from ..serializer import PersonSerializer
from ..exception import DuplicateNameError

from ..models import Person


# XXX: Filter에 관한 노트
## 만약 `CharFilter`로 다중으로 입력받고 싶다면 어떻게 해야될까?
class PersonFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name')

    age = django_filters.NumberFilter(field_name='age', lookup_expr='exact')
    age_gt = django_filters.NumberFilter(field_name='age', lookup_expr='gte')
    age_lt = django_filters.NumberFilter(field_name='age', lookup_expr='lte')

    sort = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('age', 'age'),
        ),
    )

    class Meta:
        model = Person
        fields = ['name', 'age']


class PersonListCreateAPIView(ListCreateAPIView):
    queryset = Person.objects.all().order_by('name')
    serializer_class = PersonSerializer
    filter_class = PersonFilter

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise DuplicateNameError()
