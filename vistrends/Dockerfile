FROM ubuntu:16.04

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

COPY /vt/* /opt/app/

WORKDIR /opt/app

RUN mkdir /opt/app/img

RUN mkdir /opt/app/log

RUN pip install -r requirements.txt

RUN apt-get install -y python3-tk

RUN python -m nltk.downloader all

RUN apt-get update && apt-get install -y supervisor

RUN mkdir -p /var/log/supervisor

COPY /conf/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 11071 8000

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]

