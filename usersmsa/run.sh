#!/bin/bash

# (!) Before checking if the containers with the database and kafka are running

docker build -t usersmsa_img . && docker run --rm --name usersmsa -p 8200:8000 -it usersmsa_img