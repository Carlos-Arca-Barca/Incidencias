from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


def safe_get_object(model, id, request, redirect_name):

    try:
        return model.objects.get(id=id)

    except model.DoesNotExist:

        messages.error(
            request,
            "El registro ya no existe o ha sido eliminado por otro usuario."
        )

        next_url = (
            request.POST.get("next")
            or request.GET.get("next", "")
        )

        base_url = reverse(redirect_name)

        if next_url:
            return redirect(f"{base_url}?{next_url}")

        return redirect(base_url)