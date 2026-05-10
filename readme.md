# Настройка и запуск платформы TeamFinder

## О проекте

TeamFinder — веб-сервис для поиска единомышленников и формирования команд под пет-проекты. Разработчики, дизайнеры и другие специалисты могут публиковать идеи, откликаться на предложения коллег и собирать группы для совместной работы.

**Вариант 1:** избранное и фильтрация участников по 4 критериям.

---

## Быстрый старт

### 1. Клонирование

git clone url-репозитория
cd team-finder

### 2. Виртуальное окружение

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 3. Настройка .env

cp .env_example .env

Заполните параметры в .env:
DJANGO_SECRET_KEY=ваш_ключ  # можно воспользоваться командой "openssl rand -base64 64" 
DJANGO_DEBUG=True
POSTGRES_DB=teamfinder
POSTGRES_USER=postgres
POSTGRES_PASSWORD=пароль
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
TASK_VERSION=1

### 4. База данных

docker compose up -d

### 5. Миграции и загрузка данных

python manage.py migrate
python manage.py seed_demo

### 6. Запуск

python manage.py runserver

Сайт: http://localhost:8000
Админка: http://localhost:8000/admin/

### 7. Отключение проекта

Ctrl+c - Windows
Command+c - Mac OC

docker compose down   

## Данные для входа

| Роль | Email | Пароль |
|------|-------|--------|
| Админ | igor_2007@outlook.com | 123 |
| Пользователь | albert@mail.ru | 33333 |
| Пользователь | aleks.malygin200@mail.ru | 1234567890 |
| Пользователь | svet@mail.ru | 11111 |
| Пользователь | babka@mail.ru | 22222 |

---

## Основные страницы

| Страница | URL |
|----------|-----|
| Главная (проекты) | /projects/list/ |
| Избранное | /projects/favorites/ |
| Создать проект | /projects/create-project/ |
| Детали проекта | /projects/id/ |
| Редактировать проект | /projects/id/edit/ |
| Участники | /users/list/ |
| Профиль | /users/id/ |
| Регистрация | /users/register/ |
| Вход | /users/login/ |
| Редактировать профиль | /users/edit-profile/ |
| Сменить пароль | /users/change-password/ |

---

## Особенности

- Избранное через сердечко на карточке проекта
- Фильтрация пользователей по 4 критериям (авторы избранных проектов, авторы проектов с моим участием, пользователи которым нравятся мои проекты, участники моих проектов)
- Аватар генерируется автоматически по первой букве имени
- Имя и фамилия ограничены 20 символами
- Пагинация по 12 элементов
- Кнопка Поделиться копирует ссылку в буфер обмена

---

## Права доступа

- Гость: просмотр проектов и профилей
- Пользователь: создание проектов, избранное, участие
- Админ: полный доступ через админ-панель

---

## Команды

python manage.py seed_demo        # Загрузить демо-данные
python manage.py createsuperuser  # Создать админа вручную
python manage.py makemigrations   # Создать миграции
python manage.py migrate          # Применить миграции
docker compose down               # Остановить БД

---

## Стек технологий

- Python 3.9+
- Django 4.2
- PostgreSQL 16 (Docker)
- Pillow (аватарки)
- HTML, CSS, JavaScript