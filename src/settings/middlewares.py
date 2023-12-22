from django.http.request import HttpRequest
from django.core.exceptions import PermissionDenied
from django.conf import settings


class AdminPageMiddleware:
    """
    Allows access only for auth admin or client with ADMIN_IP address
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        admin_ip = request.META.get("REMOTE_ADDR")
        if (
            request.path.startswith(f"/{settings.ADMIN_SITE_URL}")
            and admin_ip != settings.ADMIN_IP
        ):
            if not request.user.is_staff:
                raise PermissionDenied()
        return self.get_response(request)
