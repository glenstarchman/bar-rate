"""decorators for working with requests"""
import json
from django.utils import timezone
from django.core.exceptions import (PermissionDenied, ObjectDoesNotExist)
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.exceptions import ValidationError
from ..models import User
from ..views import JsonResponse
from ..serializers import MiniUserSerializer
from .exceptions import ITCCValidationException



RESPONSE_FUNCS = []


def request_user_is_user(function):
    def wrap(request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['id'])
        if user == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied()
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


class response(object):

    def __init__(self, method = ['GET'], auth_required = True):

        self.method  = method
        self.auth_required = auth_required
        self.__start = None

    def _build_meta(self):
        self.__meta['end_timestamp'] = timezone.now().timestamp() * 1000
        self.__meta['elapsed'] = self.__meta["end_timestamp"] - self.__start

    def __call__(self, function):
        def wrapped(request, *args, **kwargs):

            self.request = request
            self.__start = timezone.now().timestamp() * 1000
            self.__meta = {
                "start_timestamp": self.__start
            }
            if self.auth_required:
                if not request.user.is_authenticated():
                    end_ts = timezone.now().timestamp()
                    val = ({"errors": ["Permission Denied"]},
                        status.HTTP_401_UNAUTHORIZED)
                    self._build_meta()
                    val[0]["meta"] = self.__meta
                    return JsonResponse(*val)

            val = ()
            if request.user.is_authenticated():
                s = MiniUserSerializer(request.user)
                self.__meta['request_user'] = s.data
            else:
                self.__meta['request_user'] = None

            val = (None, status.HTTP_400_BAD_REQUEST)
            try:
                val = (function(request, *args, **kwargs),
                       status.HTTP_200_OK)
            # catch all kinds of exceptions here!
            except ObjectDoesNotExist as e:
                val = ({"errors": ["Entity does not exist"]},
                       status.HTTP_404_NOT_FOUND)
            except PermissionDenied as e:
                val = ({"errors": ["Permission Denied"]},
                       status.HTTP_401_UNAUTHORIZED)
            except ValidationError as e:
                val = ({"errors": ["Validation Error"],
                        "details": e.detail},
                       status.HTTP_400_BAD_REQUEST)
            except ITCCValidationException as e:
                val = ({"errors": e.errors},
                       status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                val = ({"errors": [str(e)]},
                       status.HTTP_400_BAD_REQUEST)

            #finally:
            self._build_meta()
            val[0]["meta"] = self.__meta
            resp = JsonResponse(*val)
            resp['Access-Control-Allow-Origin'] = '*'
            # store a tracking entry for this request
            cohort_code = request.GET.get('code', None)
            if cohort_code:
                resp.set_cookie('cohort_code', cohort_code, max_age=31536000)
            return resp

        wrapped.__doc__ = function.__doc__
        wrapped.__name__ = function.__name__
        return api_view(self.method)(wrapped)
