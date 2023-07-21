from requests import request
import json

URL_JSON_USERS = 'https://jsonplaceholder.typicode.com/users'
URL_JSON_POSTS = 'https://jsonplaceholder.typicode.com/posts'

API_ADDRESS = 'http://127.0.0.1:8200'
URL_API_USERS = API_ADDRESS + '/users'
URL_API_POSTS = API_ADDRESS + '/posts'
URL_API_LOGIN = API_ADDRESS + '/login'


def get_root_token():
    body = """{
                "username": "root",
                "password": "12345"
                }"""

    r = request('POST', URL_API_LOGIN, json=json.loads(body))

    return json.loads(r.text)['token']


def fill_users(header):
    users_json = request('GET', URL_JSON_USERS).json()
    len_users = len(users_json)
    for i, user in enumerate(users_json):

        user_dict = {
            'username': user['username'],
            'email': user['email'],
            'password': '12345qwe!',
            'first_name': user['name'].split(' ')[0],
            'last_name': user['name'].split(' ')[1]
        }

        r = request('POST', URL_API_USERS, headers=header, json=user_dict)

        print(f'{i+1} from {len_users} | username={user["username"]}, status={r.status_code}, message={r.text}')


def fill_posts(header):
    posts_json = request('GET', URL_JSON_POSTS).json()
    len_posts = len(posts_json)

    for i, post in enumerate(posts_json):
        post_dict = {
            # user root with id=1 already in database. Added user began with id=2 if database is empty
            'userid': str(int(post['userId']) + 1),
            'title': post['title'],
            'body': post['body']
        }
        r = request('POST', URL_API_POSTS, headers=header, json=post_dict)

        print(f'{i+1} from {len_posts} | post_title={post["title"]}, status={r.status_code}, message={r.text}')


if __name__ == "__main__":

    root_token = get_root_token()
    headers = {"Content-Type": "application/json; charset=utf-8", "Authorization": f"Token {root_token}"}

    fill_users(headers)

    fill_posts(headers)
