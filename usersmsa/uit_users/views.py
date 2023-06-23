import json
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
# from rest_framework import generics
# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer






#1
class UserView(APIView):
    def get(self, response):
        model = get_user_model()
        queryset = model.objects.all()
        return Response({'users': UserSerializer(queryset, many=True).data})

    def post(self, request):
        model = get_user_model()
        user_new = model.objects.create(
            username=request.data['username'],
            email=request.data['email'],
        )
        return Response({'user': model_to_dict(user_new)})

    def delete(self, ):
        pass

#2
class PostsListView(APIView):
    def get(self, request):
        return Response(json.loads(json.dumps([{"id": 1, "userid": 1, "title": "test", "body": "test body"}])))

#3
class PostsAuthorListView(APIView):
    def get(self, request, user_id):

        return Response({"user": {"id": user_id, "name": "Leanne Graham"},
                         "posts": [{"id": 1, "title": "111111", "body": "bbb11111"},
                                   {"id": 2, "title": "2222222", "body": "bbb2222222"}]})

#4
class PostAuthorView(APIView):
    def get(self, request, post_id):

        return Response({"user": {"id": 1, "name": "Leanne Graham"},
                         "post": {"id": post_id, "title": "111111", "body": "bbb11111"}})

    def post(self, request, user_id):
        pass

    def put(self, request, post_id):
        pass

    def delete(self, request, post_id):
        pass

#5
class PostsWithAuthorsListView(APIView):
    def get(self, request):

        return Response([{"user": {"id": 1, "name": "Leanne Graham"},
                         "posts": [{"id": 1, "title": "111111", "body": "bbb11111"},
                                   {"id": 2, "title": "2222222", "body": "bbb2222222"}]},
                         {"user": {"id": 2, "name": "James Hetfield"},
                          "posts": [{"id": 3, "title": "33333", "body": "bbb33333"},
                                    {"id": 4, "title": "44444", "body": "bbb444444"}]},
                         ])



