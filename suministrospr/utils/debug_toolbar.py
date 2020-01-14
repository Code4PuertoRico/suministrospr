from django.conf import settings


def show_toolbar(request):
    if request.is_ajax():
        return False

    if hasattr(request, "user") and request.user.is_superuser:
        return True

    return bool(settings.DEBUG)
