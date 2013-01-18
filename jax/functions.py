from . import signals

def signal(name, data=None):
    return signals.signal.send(None, **locals())

def jax_signal(name, data):
    return locals()

def jax_params(type='success', data=None):
    return locals()

def jax_error(message):
    return jax_params('error', message)

