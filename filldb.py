import requests
from requests import request


API_ADDRESS = 'http://127.0.0.1:8200'

def run():
    url_users = 'https://jsonplaceholder.typicode.com/users'
    url_posts = 'https://jsonplaceholder.typicode.com/posts'

    url_api_users = API_ADDRESS + '/users'
    url_api_posts = API_ADDRESS + '/posts'

    users_json = request('GET', url_users).json()
    posts_json = request('GET', url_posts).json()

    len_users = len(users_json)
    len_posts = len(posts_json)

    for i, user in enumerate(users_json):

        user_dict = {
            'username': user['username'],
            'email': user['email'],
            'first_name': user['name'].split(' ')[0],
            'last_name': user['name'].split(' ')[1]
        }

        r = request('POST', url_api_users, json=user_dict)

        print(f'{i+1} из {len_users} | username={user["username"]} request status {r.status_code}')

    for i, post in enumerate(posts_json):
        post_dict = {
            'userid': post['userId'],
            'title': post['title'],
            'body': post['body']
        }
        r = request('POST', url_api_posts, json=post_dict)

        print(f'{i+1} из {len_posts} | post_title={post["title"]} request status {r.status_code}')


if __name__ == "__main__":
    run()
