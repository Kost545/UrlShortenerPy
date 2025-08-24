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
- `app/routers/users.py` — маршруты для работы с пользователями.
- `app/routers/urls.py` — маршруты для работы с короткими ссылками пользователей.
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
    uvicorn app.main:app --reload
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
    GET /           # без параметров
    ```

- Создать пользователя:

    ```http
    POST /?user_name=имя
    ```

- Удалить пользователя:

    ```http
    DELETE /имя
    ```

### Ссылки пользователя

- Получить все ссылки пользователя:

    ```http
    GET /имя/
    ```

- Создать короткую ссылку (автоматически):

    ```http
    POST /имя/?original_url=https://example.com
    ```

- Создать короткую ссылку с кастомным коротким URL:

    ```http
    POST /имя/?original_url=https://example.com&custom_url=MyShort
    ```

- Перенаправление по короткой ссылке:

    ```http
    GET /имя/AbCdEfG
    ```

- Удалить короткую ссылку:

    ```http
    DELETE /имя/AbCdEfG
    ```

## Примечания

- Все данные хранятся в SQLite-файле `mydb.sqlite`.
- Для работы требуется Python 3.13+ и зависимости из [requirements.txt](requirements.txt).
