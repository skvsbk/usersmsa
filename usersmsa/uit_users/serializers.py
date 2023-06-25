from rest_framework import serializers
from django.contrib.auth import get_user_model


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            # password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        return user

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = ("id", "username", 'email', 'first_name', 'last_name', 'password')


class UserPostsSerializer:
    def __init__(self, user_dict, posts_list):
        self.users = user_dict
        self.posts = posts_list

    def data(self):
        return {
            "id": self.users["id"],
            "username": self.users["username"],
            "email": self.users["email"],
            "userifirst_named": self.users["first_name"],
            "last_name": self.users["last_name"],
            "posts": self.posts
        }


class UserPostsListSerializer:
    def __init__(self, user_list, posts_list):
        self.users = user_list
        self.posts = posts_list

    @staticmethod
    def serializer_posts_without_userid(post):
        return {
            "id": post['id'],
            "title": post["title"],
            "body": post["body"]
        }

    def data(self):

        result = []
        for user in self.users:
            # Grop posts by userid
            posts = list(filter(lambda post: post['userid'] == user['id'], self.posts))
            serialized_posts = list(map(self.serializer_posts_without_userid, posts))
            result.append(UserPostsSerializer(user, serialized_posts).data())

        return result
