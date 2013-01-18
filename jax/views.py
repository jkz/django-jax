"""
A bunch of decorators for returning properly formatted response data.
"""
from functools import wraps

from .errors import Error

def jax(typ='success'):
    def wrap(func):
#        @wraps(func)
        def funk(request, *args, **kwargs):
            request.jax.typ = typ
            return func(request, *args, **kwargs) or ''
        return funk
    return wrap

def render(template=None):
    _template = template

    def wrap(func):
        @wraps(func)
        def funk(request, *args, **kwargs):
            request.jax.template = _template
            data = jax('success')(func)(request, *args, **kwargs)
            if request.jax.template is None:
                raise Error('Template missing')
            return data
        return funk

    if callable(template):
        _template = None
        return wrap(template)
    return wrap

text = jax('text')
json = jax('json')
hogan = jax('hogan')

popdown = render('jax/popdown.html')

