# **Django приложение CRM системы для образовательной организации**

## Основные функции

### Управление клиентами
* Создание, просмотр, редактирование и удаление данных клиентов
* Просмотр списка клиентов
* Фильтрация клиентов, доступных для записи на курс

### Управление курсами
* Создание, просмотр, редактирование и удаление курсов
* Просмотр списка доступных курсов
* Зачисление клиентов на курсы
* Отчисление клиентов с курсов
* Просмотр студентов, зарегистрированных на конкретный курс

### Аутентификация и авторизация
* Регистрация новых пользователей
* Вход и выход из системы
* Просмотр и редактирование профиля пользователя
* Проверка аутентификации пользователя

## API эндпоинты

### Аутентификация
- `POST /api/login/` - Вход в систему
- `POST /api/logout/` - Выход из системы
- `POST /api/register/` - Регистрация нового пользователя
- `GET /api/check-auth/` - Проверка текущего статуса аутентификации
- `GET /api/profile/` - Получение профиля текущего пользователя
- `PUT /api/profile/` - Обновление профиля текущего пользователя

### Клиенты
- `GET /api/clients/` - Получение списка всех клиентов
- `POST /api/clients/` - Создание нового клиента
- `GET /api/clients/{id}/` - Получение данных о конкретном клиенте
- `PUT /api/clients/{id}/` - Обновление данных клиента
- `DELETE /api/clients/{id}/` - Удаление клиента
- `GET /api/clients/available_for_course/?course_id={id}` - Получение списка клиентов, доступных для зачисления на курс

### Курсы
- `GET /api/courses/` - Получение списка всех курсов
- `POST /api/courses/` - Создание нового курса
- `GET /api/courses/{id}/` - Получение информации о конкретном курсе, включая список зачисленных студентов
- `PUT /api/courses/{id}/` - Обновление данных курса
- `DELETE /api/courses/{id}/` - Удаление курса
- `POST /api/courses/{id}/add_students/` - Добавление студентов на курс
- `POST /api/courses/{id}/remove_student/` - Удаление студента с курса

## Установка и запуск

### Требования
- Python 3.8+
- Django 3.2+
- Django Rest Framework 3.12+
- django-cors-headers

### Шаги по установке

1. Клонируйте репозиторий:
```bash
git clone https://github.com/TheMatrix2/Django-CRM.git
cd Django-CRM
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate  # На Windows: venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Примените миграции базы данных:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

6. Запустите сервер:
```bash
python manage.py runserver
```

После выполнения этих шагов приложение будет доступно по адресу http://localhost:8000/