1. Clone both microservices (apigateway and contentsmsa) to run docker.

2. Run docker compose to run mysql server, kafka broker and zookeeper. Make sure you you enter the correct address and port for KAFKA_ADVERTISED_LISTENERS in docker-compose.yml. Also please check django.env for use correct addresses and ports. 

3. Create a database in terminal

>:/# mysql -u root -p -h 192.168.2.42 -P3306

>mysql> CREATE DATABASE uit_msa;

>mysql> exit;

4. In the terminal from the usersmsa directory, run the docker application (or just run script run.sh)

>:/# docker build -t usersmsa_img .

>:/# docker run --rm --name usersmsa -p 8200:8000 -it usersmsa_img

5. Create application database and superuser inside the container

>:/# docker exec -it usermsa bash

>root@131f47d9d234:/app# python manage.py migrate

>root@131f47d9d234:/app# python manage.py createsuperuser

>root@131f47d9d234:/app# exit

6. In the terminal from the uit_contentmsa directory, run the docker application (or just run script run.sh)

>:/# docker build -t contentmsa_img .

>:/# docker run -d --rm --network host --name contentmsa -it contentmsa_img

7. Fill the database with posts from https://jsonplaceholder.typicode.com/posts and with authors https://jsonplaceholder.typicode.com/users by script filldb.py (make sure you enter the correct address and port). Filling the database will take place through microservices.

8. Open in browser:
- http://127.0.0.1:8200/admin to login in admin panel
- http://127.0.0.1:8200/users to get all users
- http://127.0.0.1:8200/posts to get all posts
- http://127.0.0.1:8200/posts/1 to get one post with id = 1
- http://127.0.0.1:8200/authors/1 to all posts by author with id = 1
- http://127.0.0.1:8200/authors/posts to all posts by all authors

- For create user use POST request to http://127.0.0.1:8200/users
- For create post use POST request to http://127.0.0.1:8200/posts
- For update or delete post use PUT or DELETE requests http://127.0.0.1:8200/posts/1