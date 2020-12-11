from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.handlers.wsgi import WSGIRequest
from typing import Optional, Union

from users.models import Profile
from emails.models import Email
from api.serializers.user   import ProfileSerializer
from api.serializers.letter import EmailSerializer
from users.auth import get_user_id, get_current_user
from Pytreddit.redis_utils import get_redis_instance


# Class ListComments extends django_rest_framework APIView.
# Is a simple implementation of a CRUD API View
# my_email_ids
# emails_sent_by_user
class EmailsView(APIView):
    def get(
        self,
        request: WSGIRequest,
        _identificator: Optional[Union[str, int]] = None,
    ) -> Response:

        user = get_user_id()
        if user is None:
            return Response("You are not logged in. Log in to perform such actions.", status=401)
        
        email = []
        user = get_object_or_404(Profile, id=int(user))
        username = user.username
        if _identificator is not None:
            email = get_object_or_404(Email, id=_identificator)

            if username in email.to_user or username == email.from_user:
                serializer = EmailSerializer(email, many=False)
                return Response(serializer.data)
            return Response("You are not authorized to see this message.", status=401)
        try:
            if request.GET['mode'] == "inbox":
                my_mail = user.my_email_ids
                emails = []
                for i in my_mail:
                    try:
                        emails.append(get_object_or_404(Email, id=i))
                    except:
                        pass
                
                serializer = EmailSerializer(emails, many=True)
                return Response(serializer.data)
            
            elif request.GET['mode'] == "sent":
                my_mail = user.emails_sent_by_user
                emails = []
                for i in my_mail:
                    try:
                        emails.append(get_object_or_404(Email, id=i))
                    except:
                        pass
                
                serializer = EmailSerializer(emails, many=True)
                return Response(serializer.data)
        except Exception as e:
            print(e)
        my_mail = user.my_email_ids
        emails = []
        for i in my_mail:
            try:
                emails.append(get_object_or_404(Email, id=i))
            except:
                pass
        serializer = EmailSerializer(emails, many=True)
        return Response(serializer.data)

    def post(self, request: WSGIRequest) -> Response:
        if get_current_user() is None:
            return Response("You are not logged in. Log in to perform such actions.", status=401)

        _data = request.data
        if get_user_id():
            _data['from_user'] = get_current_user().username

            serializer = EmailSerializer(data=_data)
            
            for i in _data['to_user']:
                user = Profile.objects.filter(username=i)
                if len(user) == 0:
                    return Response("No such user exists.", status=status.HTTP_400_BAD_REQUEST)
            
            if serializer.is_valid():
                serializer.save()

                user = get_object_or_404(Profile, id=get_user_id())
                
                sent = user.emails_sent_by_user
                if sent is None:
                    sent = list()
                sent.append(serializer.data['id'])
                user.emails_sent_by_user = sent
                print(sent)
                user.save(update_fields=['emails_sent_by_user'])

                for i in _data['to_user']:
                    to = get_object_or_404(Profile, username=i)
                    mail = to.my_email_ids
                    if mail is None:
                        mail = list()
                    mail.append(serializer.data['id'])
                    to.my_email_ids = mail
                    to.save(update_fields=['my_email_ids'])
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def patch(
        self,
        request: WSGIRequest
    ) -> Response:
        body = request.data
        if get_user_id() is None:
            return Response("You are not logged in. Log in to perform such actions.", status=401)


        email = get_object_or_404(Email, id=body['id'])
        username = get_object_or_404(Profile, id=int(get_user_id())).username

        if username in email.to_user or username == email.from_user:
            if 'from_user' in body or 'to_user' in body:
                return Response("You can't change this field.", status=400)

            serializer = EmailSerializer(
                email,
                data = request.data,
                partial=True
            )

            if serializer.is_valid():
                user = serializer.save()
                return Response(EmailSerializer(email).data)
        
        return Response("You are not authorized to change this message.", status=401)


    def delete(
        self,
        request: WSGIRequest,
    ) -> Response:
        body = request.data
        if get_user_id() is None:
            return Response("You are not logged in. Log in to perform such actions.", status=401)

        email = get_object_or_404(Email, id=body['id'])
        username = get_object_or_404(Profile, id=int(get_user_id())).username
        if username in email.to_user or username == email.from_user:
            ident = email.id
            try:
                user_from = get_object_or_404(Profile, username=email.from_user)
                sent = user_from.emails_sent_by_user
                if sent is None:
                    sent = list()
                if ident in sent:
                    res = sent[:sent.index(ident)]
                    res.extend(sent[sent.index(ident)+1:])
                    sent = res
                    user_from.emails_sent_by_user = sent
                    user_from.save(update_fields=['emails_sent_by_user'])
            except Exception as e:
                print(e)
            print(email.to_user)
            for i in email.to_user:

                user_to = get_object_or_404(Profile, username=i)
                recieved= user_to.my_email_ids
                if recieved is None:
                    recieved = list()
                if ident in recieved:
                    res = recieved[:recieved.index(ident)]
                    res.extend(recieved[recieved.index(ident)+1:])
                    recieved = res
                    print(res)
                    user_to.my_email_ids = recieved
                    user_to.save(update_fields=['my_email_ids'])

            email.delete()

            return Response(f"You just have deleted this message")

        return Response("You are not authorized to change this message.", status=401)
        
