from django.core.exceptions import PermissionDenied


class AuthorPermissionDenied(PermissionDenied):
    status_code = 403
