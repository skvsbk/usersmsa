import json
from uuid import uuid4
from abc import ABC, abstractmethod

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from kafka import KafkaProducer, KafkaConsumer

from serializers import UserSerializer
from .serializers import UserPostsSerializer, UserPostsListSerializer
from .. import settings
from . import publisher_posts_list, publisher_post_author, publisher_posts_with_author_list, publisher_posts_author_list


class KafkaConsumerMixin:
    """ Get json from other services by Kafka"""

    @staticmethod
    def consumer_get_json(sent_key):
        consumer = KafkaConsumer(settings.KAFKA_TOPIC_CONSUMER,
                                 bootstrap_servers=f'{settings.BROKER_ADDRESS}:{settings.BROKER_PORT}',
                                 max_poll_interval_ms=10,
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


# 2
class PostsListView(APIView, KafkaConsumerMixin):
    def get(self, request):
        sent_key = uuid4().hex
        publisher_posts_list.change_state(key=sent_key,
                                          value={'name': 'get_posts_list',
                                                 'method': 'get'})
        result = self.consumer_get_json(sent_key)

        return Response(json.loads(result))

    def post(self, request):
        sent_key = uuid4().hex
        publisher_posts_list.change_state(key=sent_key,
                                          value={'name': 'get_posts_list',
                                                 'method': 'post',
                                                 'user_id': request.data['userid'],
                                                 'title': request.data['title'],
                                                 'body': request.data['body']})
        result = self.consumer_get_json(sent_key)

        return Response(json.loads(result))


# 3
class PostsAuthorListView(APIView, KafkaConsumerMixin):
    def get(self, request, user_id):
        sent_key = uuid4().hex
        publisher_posts_author_list.change_state(key=sent_key,
                                                 value={'name': 'get_authors_id_posts_list',
                                                        'method': 'get',
                                                        'user_id': user_id})
        result = self.consumer_get_json(sent_key)

        # Get user data
        model = get_user_model()
        queryset = model.objects.filter(id=user_id)
        user_data = UserSerializer(queryset, many=True).data

        # Join user data with posts list
        final_result = UserPostsSerializer(user_data[0], json.loads(result)).data()

        return Response(json.loads(json.dumps(final_result)))


# 4
class PostAuthorView(APIView, KafkaConsumerMixin):
    def get(self, request, post_id):
        sent_key = uuid4().hex
        publisher_post_author.change_state(key=sent_key,
                                           value={'name': 'get_posts_id',
                                                  'method': 'get',
                                                  'post_id': post_id})
        result = self.consumer_get_json(sent_key)

        return Response(json.loads(result))

    def put(self, request, post_id):
        """
         :param request:   {"title": "test_4 for create post",
                            "userid": 1,
                            "body": "tes_4 body"}
        :param post_id: int
        :return: json
        """

        sent_key = uuid4().hex
        publisher_post_author.change_state(key=sent_key,
                                           value={'name': 'get_posts_id',
                                                  'method': 'put',
                                                  'id': post_id,
                                                  'user_id': request.data['userid'],
                                                  'title': request.data['title'],
                                                  'body': request.data['body']})
        result = self.consumer_get_json(sent_key)

        return Response(json.loads(result))

    def delete(self, request, post_id):
        sent_key = uuid4().hex
        publisher_post_author.change_state(key=sent_key,
                                           value={'name': 'get_posts_id',
                                                  'method': 'delete',
                                                  'post_id': post_id})
        result = self.consumer_get_json(sent_key)

        return Response(json.loads(result))


# 5
class PostsWithAuthorsListView(APIView, KafkaConsumerMixin):
    def get(self, request):
        sent_key = uuid4().hex
        publisher_posts_with_author_list.change_state(key=sent_key,
                                                      value={'name': 'get_posts_with_authors_list',
                                                             'method': 'get'})
        result = self.consumer_get_json(sent_key)

        # Get user data
        model = get_user_model()
        queryset = model.objects.all().order_by("id")
        user_data = UserSerializer(queryset, many=True).data

        # Join users data with posts list
        final_result = UserPostsListSerializer(user_data, json.loads(result)).data()

        return Response(json.loads(json.dumps(final_result)))
