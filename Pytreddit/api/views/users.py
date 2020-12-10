from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.handlers.wsgi import WSGIRequest
from typing import Optional, Union

from users.models import Profile
from api.serializers.user import ProfileSerializer
from users.auth import get_user_id, is_authed_decorator

# Class ListComments extends django_rest_framework APIView.
# Is a simple implementation of a CRUD API View
class UsersView(APIView):
    def get(
        self,
        request: WSGIRequest,
        _identificator: Optional[Union[str, int]] = None,
        _username: Optional[str] = None,
        _phone: Optional[str] = None,
    ) -> Response:
        user = []
        if _identificator is not None:
            user = get_object_or_404(Profile, id=_identificator)
        elif _username is not None:
            user = Profile.objects.filter(username=_username)
        elif _phone is not None:
            user = Profile.objects.filter(phone=_phone)
        serializer = ProfileSerializer(user, many=False)

        if user is None:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(serializer.data)

    def post(self, request: WSGIRequest) -> Response:

        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @is_authed_decorator
    def patch(
        self,
        request: WSGIRequest
    ) -> Response:
        user = get_object_or_404(Profile, id=get_user_id())
        body = request.data
        if 'login' in body:
            return Response("You can't change your login.", status=400)
        serializer = ProfileSerializer(
            user,
            data = request.data,
            partial=True
        )

        if serializer.is_valid():
            user = serializer.save()
            return Response(ProfileSerializer(user).data)
        
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    @is_authed_decorator
    def delete(
        self,
        request: WSGIRequest,
        identificator: Optional[Union[str, int]] = None,
    ) -> Response:
        user = get_object_or_404(Profile, id=get_user_id())
        prev_username = str(user)

        user.delete()
        return Response(f"You just have deleted your account. Goodbye, {prev_username}!")
