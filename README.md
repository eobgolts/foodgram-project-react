# Проект Foodgram #

Проект представляет собой социальную сеть для обмена продуктовыми рецептами
Продукт написан с использованием django restframework, в качестве frontend - библиотека react


## Запуск ##

Для запуска проекта необходимо наличие директорий infra, docs и data
В директории infra необходимо разместить .env файл с необходимым набором переменных


### Пример .env файла
POSTGRES_DB='foodgram'
POSTGRES_USER='django_user'
POSTGRES_PASSWORD='mysecretpassword'
DB_NAME='foodgram'
DB_HOST='foodgram_db'
DJANGO_SECRET = 'mysecretdjangopass'
ALLOWED_HOSTS = '127.0.0.1, example.com'


Проект состоит из трёх Docker контейнеров, объединенных в один общий compose файл
Nginx в качестве gateway ожидает подключений на порт 8080

## Примеры API запросов ##

GET /api/recipes/ - получить список рецептов
POST /api/recipes/<id>/favorite/ - добавить рецепт в избранное

Полная документация API доступна по запросу <b>/api/docs/</b>

### About me ###

[Мой профиль на Github](https://github.com/eobgolts)
