from django.urls import path

from api.views.letters import EmailsView

urlpatterns = [
    path("", EmailsView.as_view()),
    path("<str:_identificator>", EmailsView.as_view()),
]
