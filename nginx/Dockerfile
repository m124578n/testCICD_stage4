FROM nginx:latest
LABEL maintainer="m23568n@gmail.com"


COPY nginx.conf /etc/nginx/nginx.conf
COPY docker-nginx-web.conf /etc/nginx/sites-available/

RUN mkdir -p /etc/nginx/sites-enabled/ && \
    ln -s /etc/nginx/sites-available/docker-nginx-web.conf /etc/nginx/sites-enabled/

CMD ["nginx", "-g", "daemon off;"]

