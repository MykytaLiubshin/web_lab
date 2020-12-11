from django.urls import path, include
from rest_framework import routers
from users.auth import login, logout

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path(
        "api-auth/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
    path("users/", include("users.urls")),
    path("emails/", include("emails.urls")),
    path("login", login),
    path("logout", logout),
    path("inbox", logout),
    path("sent", logout),

]
