from django.conf.urls import url
from django.urls import path

from .views import (
    person,
    profile,
    watch

)

from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url("^time/test$", watch.WatchListCreateView.as_view()),
    url("^person$", person.PersonListCreateAPIView.as_view()),
    path("person/<int:id>",
         person.PersonRetrieveUpdateDestroyAPIView.as_view(), name='person-detail'),

    path("person/<int:person_id>/profile", profile.ProfileAPIView.as_view(), name="profile-detail"),

    path("doc/profile", include_docs_urls(title="profile-detail"))
]
