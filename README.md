# Проект KinoZ 

Ссылка на сайт https://kinoz.ddns.net/
## Описание
Проект написанный на Django, который использует API сервер кинопоиска. Добавление новых данных из API кинопоиска (информация о фильме, скриншоты, жанры и рейтинг) в БД проекта и выдачей на странице с собственным дизайном и CSS стилями.
В далейшем по надобности добавление самого видео ролика из видео балансира через api.


## Необходимые условия

- Версия Python: 3.13
- ОС: Linux
- Менеджер пакетов: pip
- БД: SQLite

## Установка

1. создать виртуальное окружение
    ```bash 
    python -m venv venv
    ```
    ```bash 
    source venv/bin/activate
    ```
2. Установить зависимости
    ``` bash
    pip install -r requirements.txt
    ```
3. Установить миграции
    ```bash
    python manage.py migrate
    ```
4.  Создать статику 
    ```bash
    python manage.py collectstatic
    ```

[Ссылка на описание](#описание)
