import json
from django.shortcuts import get_object_or_404
from ..serializers import *
from ..models import Bartender, User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework import viewsets
from .base import build_response
from ..util import Pagination


class UserViewSet(viewsets.ViewSet):

    queryset = User.objects.all()
    pagination_class = Pagination
    paginate_by = 1
    paginate_by_param = 'page_size'
    max_paginate_by = 30

    def list(self, request):
        pass


    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        print(queryset)
        print(pk)
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return build_response(request, serializer.data)
