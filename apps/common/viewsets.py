"""
Basic building blocks for generic class based views.
"""
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from apps.common.utils import custom_response, custom_error_response


class CreateModelMixin:
    """
    Create a model instance
    """
    def create(self, request, *args, **kwargs):
        """
        create function
        :param request: request
        :param args: args
        :param kwargs: kwargs
        :return: response
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return custom_response(status=status.HTTP_201_CREATED, detail=None, data=serializer.data, headers=headers)
        return custom_error_response(status=status.HTTP_400_BAD_REQUEST, detail=list(serializer.errors.values())[0][0])

    @staticmethod
    def get_success_headers(data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class CustomModelViewSet(CreateModelMixin, GenericViewSet):
    """
    A view_set that provides default 'create()'
    """
    pass
