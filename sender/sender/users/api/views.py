import json
import logging
from typing import OrderedDict

import messagebird
import requests
import vonage
from clickatell.rest import Rest
from django.contrib.auth import get_user_model
from django.db.models import Q

# Django Rest Framework imports
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from sender.users.api.serializers import ContactsSerializer, UserSerializer
from sender.users.models import Contacts, Tokens

logger = logging.getLogger()
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False)
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class SenderView(APIView):
    serializer_class = ContactsSerializer
    permission_classes = (AllowAny,)

    def get(self, request: Request) -> Response:
        try:
            contacts = Contacts.objects.all()
            tokens = Tokens.objects.filter(active=True).first()

            if tokens is None:
                return Response({'status': 'failed', 'message': 'No tokens found'}, status=status.HTTP_400_BAD_REQUEST)

            if tokens.title == 'vonage':
                client = vonage.Client(key=tokens.token, secret=tokens.secret)
                sms = vonage.Sms(client)

                for contact in contacts:
                    if contact.already_used is True:
                        continue

                    if contact.to.endswith(".0"):
                        contact.to = contact.to.rstrip(".0")
                        contact.save()

                    sms.send_message({
                        "from": contact.from_who,
                        "to": contact.to,
                        "text": contact.text
                    })

                    contact.already_used = True
                    contact.save()

            if tokens.title == 'messagebird':
                client = messagebird.Client(tokens.token)

                for contact in contacts:
                    if contact.already_used is True:
                        continue

                    if contact.to.endswith(".0"):
                        contact.to = contact.to.rstrip(".0")
                        contact.save()

                    client.message_create(
                        contact.from_who,
                        contact.to,
                        contact.text,
                        {'reference': 'null'}
                    )

                    contact.already_used = True
                    contact.save()

            if tokens.title == 'sinch':
                # service plan: 1b19b8287a1f4242aa5391788bdaaaf7
                # secret: 1b901111a2c74ec8b4068d515d57508f
                url = f"https://sms.api.sinch.com/xms/v1/{tokens.token}/batches"
                headers = {
                    "Authorization": f"Bearer {tokens.secret}",
                    "Content-Type": "application/json"
                }

                for contact in contacts:
                    if contact.already_used is True:
                        continue

                    if contact.to.endswith(".0"):
                        contact.to = contact.to.rstrip(".0")
                        contact.save()

                    data = {
                        "from": "447520662136",
                        "to": [contact.to],
                        "body": contact.text
                    }

                    requests.post(url, headers=headers, data=json.dumps(data))

                    contact.already_used = True
                    contact.save()

            if tokens.title == 'clickatell':
                clickatell = Rest(tokens.token)

                for contact in contacts:
                    if contact.already_used is True:
                        continue

                    if contact.to.endswith(".0"):
                        contact.to = contact.to.rstrip(".0")
                        contact.save()

                    clickatell.sendMessage([contact.to], contact.text)

                    contact.already_used = True
                    contact.save()

                return Response({'status': 'success', 'message': 'Sent message'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'failed', 'message': f'Error: {e}'}, status=status.HTTP_400_BAD_REQUEST)
