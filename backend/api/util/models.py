from rest_framework.exceptions import *
from rest_framework import status

def create_model(serializer, data):
    s = serializer(data = data)
    if s.is_valid():
        s.save()
        return s.data
    else:
        raise ValidationError(detail = s.errors)

def update_model(serializer, initial, data):
    s = serializer(initial, data = data, partial = True)
    if s.is_valid():
        s.save()
        return s.data
    else:
        raise ValidationError(detail = s.errors)
