from django.db import IntegrityError

from django_filters.rest_framework import (
    filters,
    filterset
)

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from ..serializer import (
    PersonSerializer,
    PersonUpdateSerializer
)
from ..exception import DuplicateNameError

from ..models import Person

from typing import List

from django.http import HttpRequest
from django.db.models import Q


class PersonFilter(filterset.FilterSet):
    name = filters.CharFilter(field_name='name', method='filter_by_name')

    age = filters.NumberFilter(field_name='age', lookup_expr='exact')
    age_gt = filters.NumberFilter(field_name='age', lookup_expr='gte')
    age_lt = filters.NumberFilter(field_name='age', lookup_expr='lte')

    sort = filters.OrderingFilter(
        fields=(
            ('name', 'name'),
            ('age', 'age'),
        ),
    )

    class Meta:
        model = Person
        fields = ['name', 'age']

    # 만약 `CharFilter`로 Multiple Value 입력받고 싶다면 어떻게 해야될까?
    def filter_by_name(self, queryset, key: HttpRequest, value):
        """
            Note, 2022.02.05
                WSGIRequest 통해 들어온 데이터에 MultiValue 들어있기
                때문에 self.request.GET 처럼 써야함
        """
        argument = self.request.GET.copy()
        values: List = argument.getlist(key)

        if len(values) != 1:
            q = Q()
            [q.add(Q(name=value), conn_type=q.OR)
             for value in values],

            return queryset.filter(q)

        return queryset.filter(name=value)


class PersonListCreateAPIView(ListCreateAPIView):
    queryset = Person.objects.all().order_by('name')
    serializer_class = PersonSerializer
    filter_class = PersonFilter

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise DuplicateNameError()


class PersonRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.all()
    lookup_field = 'id'
    serializer_class = PersonUpdateSerializer
