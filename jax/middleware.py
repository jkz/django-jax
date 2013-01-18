from django.http import HttpResponse
from utils.decorators import receiver

from .errors import Error
from .signals import signal
from .functions import jax_signal

from utils.jsons import JsonResponse

class Jax(object):
    def __init__(self, typ=None, data=None):
        self.typ = typ
        self.data = data
        self.signals = []

        self.template = None

        def signal_handler(name, data=None, **kwargs):
            self.signals.append(jax_signal(name, data))

        receiver(signal)(self.signal)

    def signal(self, name, data=None, **kwargs):
        self.signals.append(jax_signal(name, data))

    @property
    def payload(self):
        return {'type': self.typ,
                'data': self.data,
                'signals': self.signals}

    def response(self):
        return JsonResponse(self.payload)


class JaxMiddleware:
    def process_request(self, request):
        request.jax = Jax()

    def process_exception(self, request, exception):
        if isinstance(exception, Error):
            request.jax.typ = 'error'
            return str(exception)

    def process_response(self, request, response):
        if (not hasattr(request, 'jax')
        or request.jax.typ is None
        or isinstance(response, HttpResponse)):
            return response

        if response == '':
            request.jax.data = None
        else:
            request.jax.data = response

        if request.jax.template is not None:
            from django.shortcuts import render_to_response
            from django.template import RequestContext
            return render_to_response(request.jax.template, 
                    {'jax': request.jax.payload}, RequestContext(request))
        else:
            return request.jax.response()

