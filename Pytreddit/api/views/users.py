from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.handlers.wsgi import WSGIRequest
from typing import Optional, Union

from users.models import Profile
from api.serializers.user import ProfileSerializer


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

    # def patch(
    #     self,
    #     request: WSGIRequest,
    #     identificator: Optional[Union[str, int]] = None,
    # ) -> Response:
    #     if identificator is None:
    #         return Response(
    #             "You did not specify the comment.", status=404
    #         )

    #     comment = get_object_or_404(Comment, id=identificator)
    #     serializer = CommentSerializer(
    #         comment, data=request.data, partial=True
    #     )
    #     if serializer.is_valid():
    #         comment = serializer.save()
    #         return Response(CommentSerializer(comment).data)
    #     return Response(
    #         serializer.errors, status=status.HTTP_400_BAD_REQUEST
    #     )

    # def delete(
    #     self,
    #     request: WSGIRequest,
    #     identificator: Optional[Union[str, int]] = None,
    # ) -> Response:
    #     if identificator is None:
    #         return Response(
    #             "You did not specify the comment.", status=404
    #         )
    #     comment = get_object_or_404(Comment, id=identificator)
    #     parent = Post.objects.filter(id=comment.post_id)
    #     Removing a child comment from the parent Post object

    #     _ch = parent[0].children
    #     _ch = list(filter(lambda ind: ind != comment.id, _ch))

    #     parent.update(children=_ch)
    #     comment.delete()
    #     return Response(f"Comment {identificator} deleted successfully")
