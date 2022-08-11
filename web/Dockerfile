FROM python:3.8.5
LABEL maintainer="m23568n@gmail.com"

WORKDIR /web
COPY . /web/

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt

WORKDIR /web/pdfreader_test

VOLUME /web

EXPOSE 8001

#ENTRYPOINT [ "/bin/bash", "docker-entrypoint.sh" ]
#CMD python manage.py runserver 0.0.0.0:8000

