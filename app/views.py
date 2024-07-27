from django.contrib.auth.models import User
from django.urls import resolve
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from app.exceptions import (
    IPAddressNotFoundError,
    APIKeyNotFoundError,
    ThirdPartyInvalidUUIDException,
)
from app.models import AccessApiKey
from app.permissions import IsApiKeyAuthenticated


class CheckAPIKeyAuthenticationApi(APIView):
    def get(self, request, *args, **kwargs):
        ip = request.META.get("REMOTE_ADDR")
        if not ip:
            raise IPAddressNotFoundError()

        api_key = request.headers.get("X-API-Key")
        access_api_key = AccessApiKey.objects.filter(
            key=api_key, is_enable=True
        ).first()
        if not api_key or not access_api_key:
            raise APIKeyNotFoundError()

        if not access_api_key.internal_api and ip not in access_api_key.whitelisted_ips:
            raise IPAddressNotFoundError("ip address does not have access")

        resolver_match = resolve(request.path)

        return Response(
            {"ip": ip, "api_key": api_key, "resolver_match": str(resolver_match.route)},
            status=status.HTTP_200_OK,
        )


class GetUserInformationApi(GenericAPIView):
    permission_classes = (IsApiKeyAuthenticated,)
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        uuid = request.data.get("uuid")
        user = User.objects.filter(uuid=uuid).first()
        if not user:
            raise ThirdPartyInvalidUUIDException()

        response_data = {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }

        return Response(response_data, status=status.HTTP_200_OK)
