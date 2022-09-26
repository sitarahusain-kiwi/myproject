from django.shortcuts import render
from rest_framework import status

from apps.authentication.serializers import SignUpSerializer, LoginSerializer, UserDetailSerializer
from apps.common import validation_messages
from apps.common.utils import custom_response, custom_error_response
from apps.common.viewsets import CustomModelViewSet


# Create your views here.
class SignUpViewSet(CustomModelViewSet):
    """
    Description: used for user signup
    """
    http_method_names = ('post', )
    serializer_class = SignUpSerializer

    def create(self, request, *args, **kwargs):
        """
        Add a new user with user details.
        :param request: wsgi request
        :param request: first name required and 50 characters max_length
        :param request: last name required and 50 characters max_length
        :param request: email required fields
        :param request: password required and 6 characters min length and 15 max length
        :return: User object or Error obj
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return custom_response(status=status.HTTP_201_CREATED, detail=None, data=serializer.data)
        return custom_error_response(status=status.HTTP_400_BAD_REQUEST, detail=serializer.errors)


class LoginViewSet(CustomModelViewSet):
    """
    Description: used to login user
    """
    http_method_names = ('post', )
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        """
        User login
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_obj = serializer.validated_data.get('user')
            user_obj.save()
            print(user_obj)
            serializer = self.serializer_class(user_obj).data
            data = UserDetailSerializer(user_obj).data
            data['token'] = serializer['token']
            detail = validation_messages.SUCCESS_MESSAGE['login']['success']
            return custom_response(detail=detail, data=data)
        return custom_error_response(status=status.HTTP_400_BAD_REQUEST, detail=serializer.errors)

