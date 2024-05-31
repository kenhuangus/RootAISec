from django.contrib.auth import login
from . import models


class WalletMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        address = request.META.get('HTTP_WALLET', None)
        if not address and 'wallet' in request.session:
            address = request.session['wallet']
        if address:
            request.wallet = models.Wallet.objects.get_or_create(address=address)[0]
            request.user = request.wallet.user
            login(request, request.user)
            request.session['wallet'] = address

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response