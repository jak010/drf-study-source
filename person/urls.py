from django.conf.urls import url

from .views import PersonListCreateAPIView

urlpatterns = [
    url("^person$",
        PersonListCreateAPIView.as_view())
]
