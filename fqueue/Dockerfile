#sudo docker build -t omctf/fqueue:v1.0 .
FROM ubuntu:16.04

RUN apt-get update
RUN apt-get install -y python3-pip

RUN pip3 install flask numpy redis

RUN mkdir /home/fqueue
ADD omctf-fqueue.tar.gz /home/fqueue

WORKDIR /home/fqueue

EXPOSE 5535

CMD ["python3", "/home/fqueue/app.py"]
