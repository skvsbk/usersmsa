from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status
from .serializers import UserSerializer, UserRegisterSerializer
from .validations import validation_error
from django.contrib.auth.models import User


# 1
class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        model = get_user_model()
        queryset = model.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response({'users': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):

        errors = validation_error(request.data)
        if errors is not None:
            return Response({'detail': errors}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = User.objects.get_by_natural_key(request.data['username'])
            token = Token.objects.create(user=user)
            response_serializer = UserSerializer(instance=user)
            return Response({"token": token.key, "user": response_serializer.data},
                            status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pass


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({'detail': "User not found"}, status=status.HTTP_404_NOT_FOUND)
        token, create = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    def post(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        logout(request)
        return Response(status=status.HTTP_200_OK)
