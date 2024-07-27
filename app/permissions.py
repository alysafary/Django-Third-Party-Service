from django.urls import resolve
from rest_framework.permissions import BasePermission

from app.exceptions import APINotFoundError, IPAddressNotFoundError, APIKeyNotFoundError
from app.models import AccessApiKey


class IsApiKeyAuthenticated(BasePermission):
    def has_permission(self, request, view):
        ip = self._get_ip(request)
        api_key = self._get_api_key(request)

        access_api_key = AccessApiKey.objects.filter(
            key=api_key, is_enable=True
        ).first()
        if not access_api_key or (
            not (ip in access_api_key.whitelisted_ips)
            and not access_api_key.internal_api
        ):
            return False

        request_view_name = self._get_view_name(request.path)
        if not request_view_name:
            raise APINotFoundError()

        return self.get_result(access_api_key, request_view_name)

    @staticmethod
    def get_result(access_api_key, request_view_name):
        return access_api_key.scopes.filter(views__name=request_view_name).exists()

    def _get_view_name(self, path):
        resolver_match = resolve(path)
        return resolver_match.url_name

    def _get_ip(self, request):
        ip = request.META.get("REMOTE_ADDR")
        if not ip:
            raise IPAddressNotFoundError()

        return ip

    def _get_api_key(self, request):
        api_key = request.headers.get("X-API-Key")
        if not api_key:
            raise APIKeyNotFoundError()
        return api_key
