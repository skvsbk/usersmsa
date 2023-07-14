import json
from uuid import uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from kafka import KafkaProducer, KafkaConsumer
# from rest_framework import generics
# from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserPostsSerializer, UserPostsListSerializer


class KafkaMixin:
    def kafka_exchange(self, value):
        sent_key = uuid4().hex
        producer = KafkaProducer(bootstrap_servers=f'{settings.BROKER_ADDRESS}:{settings.BROKER_PORT}',
                                 value_serializer=lambda m: json.dumps(m).encode('ascii'))

        producer.send(topic=settings.KAFKA_TOPIC_PRODUCER,
                      value=value,
                      key=sent_key.encode())
        consumer = KafkaConsumer(settings.KAFKA_TOPIC_CONSUMER,
                                 bootstrap_servers=f'{settings.BROKER_ADDRESS}:{settings.BROKER_PORT}',
                                 max_poll_interval_ms=2000,
                                 auto_offset_reset='earliest',
                                 enable_auto_commit=False, group_id='content_grp')
        result = {'details': 'Failed request'}
        for message in consumer:
            message_key = message.key.decode('utf-8')
            print('sent_key =', sent_key, '   ', 'message_key =', message_key)
            if message_key == sent_key:
                result = message.value.decode('utf-8')
                print(message.value, result)
                consumer.commit()
                consumer.close()
        return result


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


# 2
class PostsListView(APIView, KafkaMixin):
    def get(self, request):

        result = self.kafka_exchange(value={'name': 'get_posts_list', 'method': 'get'})
        return Response(json.loads(result))
    
    def post(self, request):
        """

        :param request: {
                            ;
                        }
        :return: json
        """

        result = self.kafka_exchange(value={'name': 'get_posts_list',
                                            'method': 'post',
                                            'user_id': request.data['userid'],
                                            'title': request.data['title'],
                                            'body': request.data['body']})

        return Response(json.loads(result))


# 3
class PostsAuthorListView(APIView, KafkaMixin):
    def get(self, request, user_id):
        result = self.kafka_exchange(value={'name': 'get_authors_id_posts_list',
                                            'method': 'get',
                                            'user_id': user_id})
        # Get user data
        model = get_user_model()
        queryset = model.objects.filter(id=user_id)
        user_data = UserSerializer(queryset, many=True).data

        # Join user data with posts list
        final_result = UserPostsSerializer(user_data[0], json.loads(result)).data()

        return Response(json.loads(json.dumps(final_result)))


# 4
class PostAuthorView(APIView, KafkaMixin):
    def get(self, request, post_id):
        result = self.kafka_exchange(value={'name': 'get_posts_id',
                                            'method': 'get',
                                            'post_id': post_id})

        return Response(json.loads(result))

    def put(self, request, post_id):
        """
         :param request:   {"title": "test_4 for create post",
                            "userid": 1,
                            "body": "tes_4 body"}
        :param post_id: int
        :return: json
        """

        result = self.kafka_exchange(value={'name': 'get_posts_id',
                                            'method': 'put',
                                            'id': post_id,
                                            'user_id': request.data['userid'],
                                            'title': request.data['title'],
                                            'body': request.data['body']})
        return Response(json.loads(result))

    def delete(self, request, post_id):
        result = self.kafka_exchange(value={'name': 'get_posts_id',
                                            'method': 'delete',
                                            'post_id': post_id})
        return Response(json.loads(result))


# 5
class PostsWithAuthorsListView(APIView, KafkaMixin):
    def get(self, request):
        result = self.kafka_exchange(value={'name': 'get_posts_with_authors_list',
                                            'method': 'get'})
        # Get user data
        model = get_user_model()
        queryset = model.objects.all().order_by("id")
        user_data = UserSerializer(queryset, many=True).data

        # Join users data with posts list
        final_result = UserPostsListSerializer(user_data, json.loads(result)).data()

        return Response(json.loads(json.dumps(final_result)))
