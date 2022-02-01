from django.db import IntegrityError

from rest_framework.generics import ListCreateAPIView

from ..models import Person
from ..serializer import PersonSerializer
from ..exception import DuplicateNameError


# Create your views here.

class PersonListCreateAPIView(ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise DuplicateNameError()
