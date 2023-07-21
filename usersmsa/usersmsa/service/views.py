import json
from uuid import uuid4

from rest_framework import permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from kafka import KafkaConsumer

from uit_users.serializers import UserSerializer
from .. import settings
from . import publisher_posts_list, publisher_post_author, publisher_posts_with_author_list, publisher_posts_author_list
from .transmitters import KafkaError


class KafkaConsumerMixin:
    """ Geting results in json from another services by Kafka"""

    @staticmethod
    def consumer_get_json(sent_key):
        try:
            consumer = KafkaConsumer(settings.KAFKA_TOPIC_CONSUMER,
                                     bootstrap_servers=f'{settings.BROKER_ADDRESS}:{settings.BROKER_PORT}',
                                     # max_poll_interval_ms=100,
                                     auto_offset_reset='earliest',
                                     enable_auto_commit=False, group_id=settings.KAFKA_GROUP_ID)
            KafkaError().set_error(sent_key, False)
        except Exception as e:
            # Write some log
            KafkaError().set_error(sent_key, True)
            return

        result = '{"detail": "Failed request"}'
        for message in consumer:
            try:
                message_key = message.key.decode('utf-8')
                # print('sent_key =', sent_key, '   ', 'message_key =', message_key)
                if message_key == sent_key:
                    result = message.value.decode('utf-8')
                    # print(message.value, result)
                    consumer.commit()
                    consumer.close()
            except Exception as e:
                # Write some log record
                pass

        return result


# 2
class PostsListView(APIView, KafkaConsumerMixin):
    """path: /posts"""
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, *args, **kwargs):
        sent_key = uuid4().hex
        publisher_posts_list.change_state(key=sent_key,
                                          value={'name': 'get_posts_list',
                                                 'method': 'get'})
        if KafkaError().get_error(sent_key):
            return Response(data={'detail': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        if KafkaError().get_error(sent_key):
            return Response(data={'detail': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        result = self.consumer_get_json(sent_key)

        return Response(json.loads(result))


# 3
class PostsAuthorListView(APIView, KafkaConsumerMixin):
    """path: /authors/<int:user_id>/posts"""
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, user_id):
        # Get user data
        model = get_user_model()
        queryset = model.objects.filter(id=user_id)
        user_data = UserSerializer(queryset, many=True).data

        # Send to contentmsa
        sent_key = uuid4().hex
        publisher_posts_author_list.change_state(key=sent_key,
                                                 value={'name': 'get_authors_id_posts_list',
                                                        'method': 'get',
                                                        'user_id': user_id,
                                                        'user_data': user_data[0]})
        if KafkaError().get_error(sent_key):
            return Response(data={'detail': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        result = self.consumer_get_json(sent_key)

        return Response(json.loads(result))


# 4
class PostAuthorView(APIView, KafkaConsumerMixin):
    """path: /posts/<int:post_id>"""
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, post_id):
        sent_key = uuid4().hex
        publisher_post_author.change_state(key=sent_key,
                                           value={'name': 'get_posts_id',
                                                  'method': 'get',
                                                  'post_id': post_id})
        if KafkaError().get_error(sent_key):
            return Response(data={'detail': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        result = self.consumer_get_json(sent_key)

        return Response(json.loads(result))

    def put(self, request, post_id):
        """
         :param request:   {
                            "title": "test_4 for create post",
                            "userid": 1,
                            "body": "tes_4 body"
                            }
        :param post_id: int
        :return: json
        """

        # Only owner can edit own posts
        if request.user.id != int(request.data['userid']):
            return Response({'detail': 'Unable to edit non-own post'}, status=status.HTTP_403_FORBIDDEN)

        sent_key = uuid4().hex
        publisher_post_author.change_state(key=sent_key,
                                           value={'name': 'get_posts_id',
                                                  'method': 'put',
                                                  'id': post_id,
                                                  'user_id': request.data['userid'],
                                                  'title': request.data['title'],
                                                  'body': request.data['body']})
        if KafkaError().get_error(sent_key):
            return Response(data={'detail': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        result = self.consumer_get_json(sent_key)

        return Response(json.loads(result))

    def delete(self, request, post_id):

        # Only owner can delete own posts
        if request.user.id != int(request.data['userid']):
            return Response({'detail': 'Unable to delete non-own post'}, status=status.HTTP_403_FORBIDDEN)

        sent_key = uuid4().hex
        publisher_post_author.change_state(key=sent_key,
                                           value={'name': 'get_posts_id',
                                                  'method': 'delete',
                                                  'post_id': post_id})
        if KafkaError().get_error(sent_key):
            return Response(data={'detail': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        result = self.consumer_get_json(sent_key)

        return Response(json.loads(result))


# 5
class PostsWithAuthorsListView(APIView, KafkaConsumerMixin):
    """path: /authors/posts"""
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request):
        # Get user data
        model = get_user_model()
        queryset = model.objects.all().order_by("id")
        user_data = UserSerializer(queryset, many=True).data

        sent_key = uuid4().hex
        publisher_posts_with_author_list.change_state(key=sent_key,
                                                      value={'name': 'get_posts_with_authors_list',
                                                             'method': 'get',
                                                             'user_data': user_data})
        if KafkaError().get_error(sent_key):
            return Response(data={'detail': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        result = self.consumer_get_json(sent_key)

        return Response(json.loads(result))
