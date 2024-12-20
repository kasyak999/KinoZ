# Проект KinoZ 

Ссылка на сайт https://kinoz.ddns.net/ (не работает)
## Описание
Проект написанный на Django, который использует API сервер кинопоиска. Добавление новых данных из API кинопоиска (информация о фильме, скриншоты, жанры и рейтинг) в БД проекта и выдачей на странице с собственным дизайном и CSS стилями.
В дальнейшем по надобности добавление самого видео ролика из видео балансира через api.

Из-за ограничений кинопоиска на 500 запросов в сутки, реализован такой процесс:
- если фильма нет в базе, то он автоматически добавляется в базу, что бы админ проверил правильность заполнения полей. У пользователя будет только информация об успешном добавлении фильма. И повторно пользователь не сможет отправлять запрос к api кинопоиска.
- после проверки фильм публикуется на самом сайте и доступен для просмотра и комментариям

Таким образом отправляется только 2 запроса к кинопоиску с одним фильмом, скриншотами и повторных запросов не будет с данным фильмом.

В дальнейшем планирую:
-  добавить еще один api балансир фильмов который будет по такому же принципу добавлять видео ролик.
- добавить рейтинг фильма, который будет изначально браться с кинопоиска и суммироваться с оценками пользователей проекта.
- Исправить шаблон сайта.
- оптимизировать работу проекта
- оптимизировать код
- подготовить docker-compose.production.yml
- настроить CI/CD на GitHub Actions

## Технологии проекта
- Python 3.13
- MySQL
- Ngnix
- Django 5.1.2

## Необходимые условия

- Docker
- ОС: Linux

## Установка и запуск

1. Создать файл **.env** с содержимым:
```bash
SECRET_KEY=ключ_джанго_проекта
MYSQL_DATABASE=my_database
MYSQL_USER=user
MYSQL_PASSWORD=user_password   
MYSQL_ROOT_PASSWORD=root_password
MYSQL_PORT=3306
MYSQL_HOST=db_mysql
```
2. Запустить docker compose
```bash 
docker compose up
```
или
```bash
docker compose up --build 
```

[Ссылка на описание](#описание)
