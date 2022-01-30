from .models import Person
from rest_framework.generics import ListCreateAPIView
from .serializer import PersonSerializer


# Create your views here.

class PersonListCreateAPIView(ListCreateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
