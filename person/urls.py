from django.conf.urls import url

from .views import (
    person,
    watch

)

urlpatterns = [
    url("^person$", person.PersonListCreateAPIView.as_view()),

    url("^time/test$", watch.WatchListCreateView.as_view())

]
