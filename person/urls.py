from django.conf.urls import url
from django.urls import path

from .views import (
    person,
    watch

)

urlpatterns = [
    url("^person$", person.PersonListCreateAPIView.as_view()),
    path("person/<int:id>",
         person.PersonRetrieveUpdateDestroyAPIView.as_view(), name='person_detail_view'),

    url("^time/test$", watch.WatchListCreateView.as_view())

]
