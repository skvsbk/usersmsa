from django.conf import settings
from django.contrib.auth import get_user_model
from django.forms import model_to_dict

# from rest_framework import generics
# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer


# 1
class UserView(APIView):
    def get(self, request):
        model = get_user_model()
        queryset = model.objects.all()
        return Response(UserSerializer(queryset, many=True).data)

    def post(self, request):
        model = get_user_model()
        user_new = model.objects.create(
            username=request.data['username'],
            email=request.data['email'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],

        )
        return Response(model_to_dict(user_new, exclude=['password', 'last_login', 'is_superuser', 'is_staff',
                                                         'is_active', 'date_joined', 'groups', 'user_permissions']))

    def delete(self, ):
        pass


