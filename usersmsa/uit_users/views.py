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
from .serializers import UserSerializer


producer = KafkaProducer(bootstrap_servers=f'{settings.BROKER_ADDRESS}:{settings.BROKER_PORT}',
                         value_serializer=lambda m: json.dumps(m).encode('ascii'))



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
        sent_key = uuid4().hex
        producer.send(topic=settings.KAFKA_TOPIC_PRODUCER,
                      value={'name': 'get_posts_list'},
                      key=sent_key.encode())
        consumer1 = KafkaConsumer(settings.KAFKA_TOPIC_CONSUMER,
                                  bootstrap_servers=f'{settings.BROKER_ADDRESS}:{settings.BROKER_PORT}',
                                  # request_timeout_ms=12000,
                                  max_poll_interval_ms=2000,
                                  auto_offset_reset='earliest',
                                  enable_auto_commit=False, group_id='content_grp')
        result = {'detail': 'Failed request'}
        for message in consumer1:
            message_key = message.key.decode('utf-8')
            print('sent_key =', sent_key, '   ', 'message_key =', message_key)
            if message_key == sent_key:
                result = message.value.decode('utf-8')
                print(message.value, result)
                consumer1.commit()
                consumer1.close()

        return Response(json.loads(result))
#3
class PostsAuthorListView(APIView):
    def get(self, request, user_id):
        sent_key = uuid4().hex
        producer.send(topic=settings.KAFKA_TOPIC_PRODUCER,
                      value={'name': 'get_authors_id_posts_list', 'user_id': user_id, 'method': 'get'},
                      key=sent_key.encode())

        consumer1 = KafkaConsumer(settings.KAFKA_TOPIC_CONSUMER,
                                  bootstrap_servers=f'{settings.BROKER_ADDRESS}:{settings.BROKER_PORT}',
                                  # request_timeout_ms=12000,
                                  max_poll_interval_ms=2000,
                                  auto_offset_reset='earliest',
                                  enable_auto_commit=False, group_id='content_grp')
        result = {'detail': 'Failed request'}
        for message in consumer1:
            message_key = message.key.decode('utf-8')
            print('sent_key =', sent_key, '   ', 'message_key =', message_key)
            if message_key == sent_key:
                result = message.value.decode('utf-8')
                print(message.value, result)
                consumer1.commit()
                consumer1.close()

        return Response(json.loads(result))

#4
class PostAuthorView(APIView):
    def get(self, request, post_id):
        sent_key = uuid4().hex
        producer.send(topic=settings.KAFKA_TOPIC_PRODUCER,
                      value={'name': 'get_posts_id', 'post_id': post_id, 'method': 'get'},
                      key=sent_key.encode())

        consumer1 = KafkaConsumer(settings.KAFKA_TOPIC_CONSUMER,
                                  bootstrap_servers=f'{settings.BROKER_ADDRESS}:{settings.BROKER_PORT}',
                                  # request_timeout_ms=12000,
                                  max_poll_interval_ms=2000,
                                  auto_offset_reset='earliest',
                                  enable_auto_commit=False, group_id='content_grp')
        result = {'detail': 'Failed request'}
        for message in consumer1:
            message_key = message.key.decode('utf-8')
            print('sent_key =', sent_key, '   ', 'message_key =', message_key)
            if message_key == sent_key:
                result = message.value.decode('utf-8')
                print(message.value, result)
                consumer1.commit()
                consumer1.close()

        return Response(json.loads(result))

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



