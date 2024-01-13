from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpResponseRedirect
from django.urls import reverse


class MyAccountAdapter(DefaultAccountAdapter):
    def get_email_confirmation_url(self, request, emailconfirmation):
        relative_url = reverse(
            "auths:account_confirm_email", args=[emailconfirmation.key]
        )
        return request.build_absolute_uri(relative_url)

    def respond_email_verification_sent(self, request, user):
        return HttpResponseRedirect(
            reverse("auths:account_email_verification_sent")
        )
