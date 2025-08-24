# FastAPI URL Shortener

Простой сервис сокращения ссылок на FastAPI и aiosqlite.

## Возможности

- Асинхронный HTTP API на FastAPI.
- Хранение пользователей и ссылок в SQLite (через aiosqlite).
- Генерация коротких ссылок с помощью SHA-256 + base64.
- Пользовательские профили: каждый пользователь может создавать свои короткие ссылки.
- Получение, удаление пользователей и ссылок.
- Перенаправление по короткой ссылке.

## Структура проекта

- `app/main.py` — точка входа, инициализация БД, подключение роутеров.
- `app/routers/users.py` — все маршруты для работы с пользователями и их ссылками.
- `app/db_requests.py` — SQL-запросы для работы с БД.
- `app/logics.py` — логика генерации коротких ссылок.
- `mydb.sqlite` — база данных (создаётся автоматически).
- `Dockerfile` — для запуска через Docker.

## Установка и запуск

1. Клонируйте репозиторий:

    ```sh
    git clone <repo-url>
    cd <repo-directory>
    ```

2. Установите зависимости:

    ```sh
    pip install -r requirements.txt
    ```

3. Запустите сервер локально:

    ```sh
    fastapi dev app/main.py
    ```

4. (Опционально) Соберите и запустите через Docker:

    ```sh
    docker build -t urlshortener:dev .
    docker run --rm -p 8000:8000 --name urlshortener urlshortener:dev
    ```

## Примеры запросов

### Пользователи

- Получить список пользователей:

    ```http
    GET /users/
    ```

- Создать пользователя:

    ```http
    POST /users/?user_name=имя
    ```

- Удалить пользователя:

    ```http
    DELETE /users/имя
    ```

### Ссылки пользователя

- Получить все ссылки пользователя:

    ```http
    GET /users/имя/urls/
    ```

- Создать короткую ссылку:

    ```http
    POST /users/имя/urls/?original_url=https://example.com
    ```

- Перенаправление по короткой ссылке:

    ```http
    GET /users/имя/urls/AbCdEfG
    ```

- Удалить короткую ссылку:

    ```http
    DELETE /users/имя/urls/AbCdEfG
    ```

## Примечания

- Все данные хранятся в SQLite-файле `mydb.sqlite`.
- Для работы требуется Python 3.13+ и зависимости из [requirements.txt](requirements.txt).
