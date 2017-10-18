FROM python:3.5-alpine
#FROM python:3.5-jessie
ADD ./ /sb/

RUN echo "@community http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories

RUN apk add --update --no-cache ca-certificates gcc g++ curl openblas-dev@community

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

#RUN pip install --upgrade pip

RUN pip install -r /sb/requirements.txt

WORKDIR /sb/app/

RUN sed -i -e 's/redis_ip : localhost/redis_ip : redis/g' ./config.cfg
RUN sed -i -e 's/mongo_ip : localhost/mongo_ip : mongo/g' ./config.cfg

CMD ["python3", "./app.py"]