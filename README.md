# Структура проекта

- `templates` — Папка с html файлом для отображения апи + JS
- `tests` — Тесты
- `modules/users` — Django приложение

# Установка Django

## Требования к рабочему окружению

- Python 3.8 +
- PostgreSQL


## Установка
Для Linux (и macOS):
Создаем virtualenv и активируем его:
```bash
mkvirtualenv venv
workon venv
```
для Windows:
Создаем virtualenv и активируем его:
```bash
python -m venv venv
venv\Scripts\activate 
```
Устанавливаем зависимости Django:
```bash
cd backend
pip install -r requirements.txt
```

Создаем файл .env со следующим содержимым:
```
DEBUG=True
SECRET_KEY='django-insecure-8w0f%85^2v9y!w1gpx(&mb28**a8cxr_&xfa6u!^p2$!&72n%*'
DB_NAME=hammer_db
DB_USER=hammer_db
DB_PASSWORD=hammer_db
DB_HOST=localhost
DB_PORT=5432
```

Создаем БД:
Подключитесь к PostgreSQL:

Откройте терминал и подключитесь к PostgreSQL под суперпользователем (например, postgres):
```bash
psql -U postgres
```
Если PostgreSQL защищён паролем, введите его при запросе.

Создайте базу данных с именем hammer_db:
```bash
CREATE DATABASE hammer_db;
```
Создайте пользователя с именем hammer_db и задайте пароль:
```bash
CREATE USER hammer_db WITH PASSWORD 'hammer_db';
```
Предоставьте пользователю hammer_db полный доступ к базе данных hammer_db:
```bash
GRANT ALL PRIVILEGES ON DATABASE hammer_db TO hammer_db;
```
суперправа:
```bash
ALTER USER hammer_db WITH SUPERUSER;
```
```

Сделайте тесты
```bash
python manage.py test
```


Django готов к запуску.

## Запуск Django

Запустить приложение можно через командную строку:
```bash
python manage.py runserver
```


После запуска, проект будет доступен локально по адресам:

- http://127.0.0.1:8000/swagger/ # путь для Swagger UI
- http://127.0.0.1:8000/redoc/   # путь для Redoc
- http://127.0.0.1:8000/api/phone_auth_html/ # путь апи, динамическое обновлдение кода и профиль при запросе по номеру телефона
- http://127.0.0.1:8000/api/auth/ # авторизация
- http://127.0.0.1:8000/api/profile/ # профиль

## Работа апи
1. Отправьте код подтверждения
Phone Number: # Ваш номер телефона

2. Проверьте код
Phone Number: # Ваш номер телефона;
Verification Code: # Ваш код подтвреждения, динамически отобразится на странице

4. Профиль пользователя по номеру.
Phone Number: # При вводе номера выдаст данные по номеру

5. Активируйте инвайт-код
Phone Number: # Номер телефона;
Invite Code: # инвайт-код

## Postman коллекция и окружение. Два файла 

https://disk.yandex.ru/d/o4E_QB3BxldU6A

## Задеплоил на pythonanywhere. Можно сразу потестить
https://pavlowave.pythonanywhere.com/api/phone_auth_html/
