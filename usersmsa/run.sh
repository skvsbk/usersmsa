!#/bin/bash

# (!) Before checking if the containers with the database and kafka are running

docker build -t uit_apigateway_img . && docker run --name uit_apigateway -it -p 8200:8000  uit_apigateway_img