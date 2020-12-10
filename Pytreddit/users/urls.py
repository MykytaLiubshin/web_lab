from django.urls import path

from api.views.users import UsersView

urlpatterns = [
    path("", UsersView.as_view()),
    path("<str:_identificator>", UsersView.as_view()),
]
