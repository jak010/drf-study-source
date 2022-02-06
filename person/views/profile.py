from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from ..serializer import (
    ProfileUpdateSerializer
)

from ..models import PersonProfile


class ProfileAPIView(ListCreateAPIView):
    # queryset = PersonProfile.objects.all()
    serializer_class = ProfileUpdateSerializer
    lookup_url_kwarg = 'person_id'

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'person_id': self.kwargs.get(self.lookup_url_kwarg)
        }
