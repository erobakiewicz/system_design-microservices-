```Description```

Microservice API application managed by Kubernetes and run on Flask, Python functions and RabbitMQ for the queue.
It takes a video file and returns an audio (mp3) file sent to the user's email.

Uses MongoDB with GridFS for storing files and MySQL for storing users and their data.

Users are authenticated using basic auth and JWT tokens.


```How to run```
Requirements:
- Docker
- Kubernetes
- Minikube (and Ingress addon enabled)
- MongoDB and MYSQL databases

1. Clone the repository
2. Run SQL script in 'auth' directory to create database and tables and initial data
3. Run ```kubectl apply -f DIRECTORY``` for each directory 'manifests':
    - auth
    - converter
    - gateway
    - notification
    - rabbit

Made following course "Microservice Architecture and System Design with Python & Kubernetes" by freeCodeCamp.org