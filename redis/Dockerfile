#sudo docker build -t omctf/redis:v1.0 .
FROM ubuntu:16.04

RUN mkdir /home/redis
ADD redis-3.0.0.tar.gz /home/redis

RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y libcurl3

RUN cd /home/redis && make && make install 
RUN ldconfig
RUN mkdir /etc/redis
RUN cp /home/redis/redis.conf /etc/redis

VOLUME ["/data"]

WORKDIR /data

EXPOSE 6379

CMD ["redis-server", "/etc/redis/redis.conf"]

