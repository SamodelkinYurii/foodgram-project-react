![Python](https://img.shields.io/badge/Python-3670A0?style=flat&logo=python&logoColor=ffdd54)
![Nginx](https://img.shields.io/badge/Nginx-%23009639.svg?style=flat&logo=nginx&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-%23323330.svg?style=flat&logo=javascript&logoColor=%23F7DF1E)
![Django](https://img.shields.io/badge/Django-%23092E20.svg?style=flat&logo=django&logoColor=white)
![Django Rest Framework](https://img.shields.io/badge/Django%20Rest%20Framework-ff1709?style=flat&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-%23316192.svg?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-%23121011.svg?style=flat&logo=github&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-%232671E5.svg?style=flat&logo=githubactions&logoColor=white)
![example workflow](https://github.com/SamodelkinYurii/foodgram-project-react/actions/workflows/main.yml/badge.svg)


# Проект Foodgram – Продуктовый помощник

Любой пользователь может зайти на сайт и посмотреть интересные, вкусные, полезные рецепты.

А для зарегестрированных пользователей открываются гораздо большн возможностей:
- создание собственных рецептов и их редактирование;
- сохранение рецептов других пользователей в _"Избранное"_;
- создание _списков покупок_ необходимых ингредиентов для понравившегося Вам блюда;
- подписки на авторов;
- и многое другое, о них вы сможете узнать после регистрации✨. 


## Как запустить проект

1. Клонируем себе репозиторий:

```bash 
git clone <ваша ссылка на репозиторий>
```
2. Переходим в директорию foodgram-project-react, создаем файл .env и заполняем его.
```bash
cd foodgram-project-reac
```

3. Запускаем проект:

```bash
docker compose -f docker-compose.yml up
```

4. После запуска выполняем миграции, сбор статических файлов, а также выгрузку ингредиентов в базу данных. По желанию можно создать суперпользователя:

```bash
docker compose -f docker-compose.yml exec backend python manage.py migrate

docker compose -f docker-compose.yml exec backend python manage.py collectstatic

docker compose -f docker-compose.yml exec backend python manage.py load_data

docker compose -f docker-compose.yml exec backend python manage.py createsuperuser
```

5. Проект будет доступен по данной ссылке - <http://localhost:7000/>, а документация к API - <http://localhost:7000/api/docs/>

## Как создать и загрузить Docker образы

1.  Меняем username на ваш логин в DockerHub:

```bash
docker build -t username/foodgramm_frontend:latest frontend/

docker build -t username/foodgramm_backend:latest backend/

docker build -t username/foodgramm_gateway:latest nginx/
```

2. Загружаем образы на DockerHub:

```bash
docker push username/foodgramm_backend:latest

docker push username/foodgramm_frontend:latest

docker push username/foodgramm_gateway:latest
```

## Как задеплоить проект на сервер

1. Подключаемся к удаленному серверу. У вас должен быть установлен Nginx. Устанавливаем Docker Compose:

```bash
sudo apt update

sudo apt install curl

curl -fSL https://get.docker.com -o get-docker.sh

sudo sh ./get-docker.sh

sudo apt install docker-compose-plugin 
```

2. Создаем на сервере директорию и переходим в нее:

```bash
mkdir foodgram

cd foodgram
```

3. В директорию foodgram/ копируем файлы docker-compose.production.yml (Не забываем менять username image-образов!), nginx.conf и .env.

4. Запускаем docker compose:

```bash
sudo docker compose -f docker-compose.production.yml up -d
```

5. После запуска выполняем миграции, сбор статических файлов, а также выгрузку ингредиентов в базу данных. По желанию можно создать суперпользователя:

```bash
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate

sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic

sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/static/. /backend_static/static/ 

sudo docker compose -f docker-compose.production.yml exec backend python manage.py load_data

sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```

6. В редакторе nano открываем конфигурацию Nginx, а затем добавляем следующие настройки:

```bash
sudo nano /etc/nginx/sites-enabled/default

location / {
    proxy_set_header Host $http_host;
    proxy_pass http://127.0.0.1:7000;
}
```

7. Проверяем работоспособность и перезапускаем Nginx:

```bash
sudo nginx -t

sudo service nginx reload
```

## Как настроить CI/CD

Добавляем секреты в GitHub Actions:
- DOCKER_USERNAME - никнейм в DockerHub
- DOCKER_PASSWORD - пароль в DockerHub
- HOST - ip-адрес сервера
- USER - имя пользователя
- SSH_KEY - закрытый ssh-ключ сервера
- SSH_PASSPHRASE - пароль для ssh-ключа
- TELEGRAM_TO - id аккаунта в Телеграме
- TELEGRAM_TOKEN - токен вашего бота
- SECRET_KEY - секретный ключ проекта
- DEBUG - режим отладки
- ALLOWED_HOSTS - список разрешённых хостов для запуска проекта

## Автор проекта

Проект доступен по адресу: [samod3.hopto.org](https://samod3.hopto.org)