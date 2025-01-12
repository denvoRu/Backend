FROM nginx:latest

# Устанавливаем Apache Utils для htpasswd
RUN apt-get update && apt-get install -y apache2-utils && apt-get clean

# Создаём пользователя для htpasswd
ARG USERNAME=selenium
ARG PASSWORD=selenium

RUN htpasswd -bc /etc/nginx/.htpasswd selenium $SELENIUM_HUB_PASSWORD

# Копируем конфиг Nginx
COPY nginx.conf /etc/nginx/nginx.conf
