# order-monitor
order-monitor - Приложение для мониторинга заказов импортированные из Google Sheet.

# Стек
- Python 3.10
- Django 4.0
- Django Rest Framework
- Celery
- Postgres
- Google Sheet API
- Docker

# Как развернуть проект
Есть два способа - Docker, для продакшена, и локально, для разработки/тестов.

## Docker
1. Клонируйте проект
    ```bash
    $ git clone <url_to_git>
    ```
2. Создайте файл `.env` как в [примере](.env_example).

3. Установите docker и docker-compose, если не установленно на машине. И запустите:
    ```bash
    $ sudo docker-compose -f docker-compose.prod.yaml up -d
    ```

4. Примените миграции и соберите статику:
    ```bash
    $ sudo docker-compose -f docker-compose.prod.yaml exec web python manage.py migrate
    $ sudo docker-compose -f docker-compose.prod.yaml \ 
    exec web python manage.py collectstatic
    ```
Готово! Теперь приложение доступно по адресу http://localhost/.

## Локально 
1. Клонируйте проект
    ```bash
    $ git clone <url_to_git>
    ```
2. Установите python 3.10 и требуемые pip-покеты в окружение:
    ```bash
    $ python -m venv venv && . venv/bin/activate
    $ pip install -r requirements.txt
    ```

3. Установите docker и docker-compose, если не установленно на машине. И запустите:
    ```bash
    $ sudo docker-compose -f docker-compose.local.yaml up -d
    ```
4. Запустите приложение:
    ```bash
    $ python manage.py runserver
    ```
Готово! Теперь приложение доступно по адресу http://localhost:8000/.
