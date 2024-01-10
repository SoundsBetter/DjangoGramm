import typing as t
from django.contrib import messages
from django.db.models import Model
from django.shortcuts import redirect, get_object_or_404

from DjangoGramm.text_messages import NOT_HAVE_ACCESS

M = t.TypeVar("M", bound=Model)


class UserIsOwnerMixin:
    object: M = None
    model: M = None

    def dispatch(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.model, pk=kwargs["pk"])

        owner = (
            self.object.user
            if hasattr(self.object, "user")
            else self.object.post.user
        )

        if request.user != owner:
            messages.error(request, NOT_HAVE_ACCESS)
            return redirect(request.META.get("HTTP_REFERER", "home"))
        return super().dispatch(request, *args, **kwargs)  # type:ignore
