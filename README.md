# Тестовое задание 
# DRF Custom Auth Project

Проект реализует кастомную систему аутентификации и авторизации

## Структура проекта
```
TZ_auth_login/
├── README.md
├── requirements.txt
├── manage.py
├── project/
│ ├── __init__.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
├── auth_app/
│ ├── __init__.py
│ ├── apps.py
│ ├── models.py
│ ├── serializers.py
│ ├── views.py
│ ├── middleware.py
│ ├── permissions.py
│ └── utils.py
├── access_control/
│ ├── __init__.py
│ ├── apps.py
│ ├── models.py
│ ├── serializers.py
│ └── views.py
├── mock_app/
│ ├── __init__.py
│ └── views.py
└── fixtures/
 └── initial_data.json
```


Запуск локально:
1. Склонируйте репозиторий, создайте виртуальное окружение и установите зависимости:
```
git clone https://github.com/Fitness-Developer/TZ_auth_login.git
cd TZ_auth_login
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Инициализируйте проект и создайте суперпользователя (миграции):
```
python manage.py makemigrations 
python manage.py migrate
python manage.py loaddata fixtures/initial_data.json
python manage.py runserver
```

# Доступные эндпоинты (ключевые):
- POST /api/auth/register — регистрация
- POST /api/auth/login/ — логин (возвращает token)
- POST /api/auth/logout/ — логаут (удаляет токен)
- PUT /api/auth/user/ — обновление своего профиля
- DELETE /api/auth/user/ — удаление аккаунта
# Admin API (только роль admin может):
- GET/POST /api/admin/roles/
- GET/POST /api/admin/resources/
- POST /api/admin/assign-permission/
- POST /api/admin/assign-role/
# Mock resources:
- GET /api/mock/products/
- GET /api/mock/orders/

Все API проверял через Postman
Авторизация: передавайте заголовок Authorization: Token <token>
