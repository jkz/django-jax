from django.dispatch import Signal

signal = Signal(providing_args=['name', 'data'])

