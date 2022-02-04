import http

from django.db import IntegrityError

from django_filters.rest_framework import filters, filterset

from rest_framework.generics import ListCreateAPIView
from ..serializer import PersonSerializer
from ..exception import DuplicateNameError

from ..models import Person

from typing import List

from django.core.handlers.wsgi import WSGIRequest
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

    # 만약 `CharFilter`로 MultipleValue로 입력받고 싶다면 어떻게 해야될까?
    def filter_by_name(self, queryset, key: HttpRequest, value):
        q = Q()

        argument = self.request.GET.copy()
        names: List = argument.getlist(key)

        if len(names) != 1:
            [q.add(Q(name=value), conn_type=q.OR)
             for value in names],
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
