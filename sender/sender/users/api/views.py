import logging
from typing import OrderedDict

import vonage
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
from sender.users.models import Contacts

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
            client = vonage.Client(key="b0bc2441", secret="VKxfdTfkP3YNMXK5")
            sms = vonage.Sms(client)

            for contact in contacts:
                if contact.already_used is True:
                    continue

                sms.send_message({
                    "from": contact.from_who,
                    "to": contact.to,
                    "text": contact.text
                })

                contact.already_used = True
                contact.save()

            return Response({'status': 'success', 'message': 'Sent message'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'failed', 'message': f'Error: {e}'}, status=status.HTTP_400_BAD_REQUEST)

