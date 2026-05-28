from django.db.models.deletion import ProtectedError
from django.contrib import messages


def safe_delete(request, obj, redirect_url):
    """
    Eliminación segura centralizada para todo el ERP.
    """

    try:
        obj.delete()
        return True, redirect_url

    except ProtectedError:
        messages.error(
            request,
            "No se puede eliminar este registro porque está siendo utilizado en otra tabla."
        )
        return False, redirect_url