from ..models import Watch
from ..serializer import WatchSerializer

from rest_framework.generics import ListCreateAPIView


class WatchListCreateView(ListCreateAPIView):
    queryset = Watch.objects.all()
    serializer_class = WatchSerializer
