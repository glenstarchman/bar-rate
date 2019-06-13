import json
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from ..serializers import *
from ..models import Bartender, User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from .base import build_response
from ..util import Pagination
from .taggable import TaggableViewSet
from ..serializers.user import *
from ..serializers.mini_serializers import MiniUserSerializer

class UserViewSet(TaggableViewSet):

    queryset = User.objects.all()
    pagination_class = Pagination
    paginate_by = 1
    paginate_by_param = 'page_size'
    max_paginate_by = 30

    def list(self, request):
        pass


    def retrieve(self, request, pk=None):
        """return a single user"""
        queryset = User.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return build_response(request, serializer.data)


    def create(self, request):
        """create a user. Will also create a user from social auth later"""
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        serializer = CreateUserSerializer(data=body)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(body['email'], password=body['password'],
                                first_name=body['first_name'],
                                last_name=body['last_name'],
                                username=body['username'],
                               )
        ser = LoginUserSerializer(user)
        return build_response(request, ser.data)


    @action(detail=False, methods=['post'])
    def login(self, request):
        #TODO: this needs to add in support for social login later
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body['username']
        password = body['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
        else:
            raise(AuthenticationFailed(detail="Invalid Credentials"))
        ser = LoginUserSerializer(instance=user)
        return build_response(request, ser.data)

    @action(detail=False, methods=['POST'])
    def reset_token(self, request):
        """resets an authenticated user's auth token"""
        pass


    @action(detail=False, methods=['get',])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return build_response(request, serializer.data)
