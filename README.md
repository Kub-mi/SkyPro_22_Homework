# SkyPro Homework — Django Project

Учебный проект для курса по Django.  
Реализован каталог продуктов с возможностью регистрации пользователей, созданием/редактированием товаров и системой прав доступа.

---

## Установка и запуск проекта

### 1. Клонирование репозитория
```bash
git clone <https://github.com/Kub-mi/SkyPro_22_Homework.git>
cd SkyPro_22_Homework
```

### 2. Создание виртуального окружения и установка зависимостей
```bash
python3 -m venv .venv
source .venv/bin/activate     # для Linux/macOS
.venv\Scripts\activate      # для Windows PowerShell

pip install -r requirements.txt
```

### 3. Применение миграций и создание суперпользователя
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Запуск сервера разработки
```bash
python manage.py runserver
```

---

## Пользователи и аутентификация

- Используется **кастомная модель пользователя**: `users.CustomUser`.
- Авторизация доступна по адресу:  
  `http://127.0.0.1:8000/accounts/login/`

### Настройки аутентификации
В `settings.py` определены:
```python
LOGIN_URL = "users:login"
LOGIN_REDIRECT_URL = "catalog:home"
LOGOUT_REDIRECT_URL = "catalog:home"
```

> Вьюхи, требующие авторизации, используют `LoginRequiredMixin`. Переадресации на логин происходят по имени маршрута из `LOGIN_URL`.

---

## Права доступа

### Владелец продукта
- Может редактировать и удалять **только свои** продукты.
- При создании продукта владелец проставляется автоматически (в `CreateView` значение берётся из `request.user`).

### Группа «Модератор продуктов»
Для модераторов добавлены специальные права:
- `catalog.can_unpublish_product` — **отмена публикации** продукта (кастомное право из `Product.Meta.permissions`).
- `catalog.delete_product` — **удаление любого** продукта (стандартное модельное право).

---

## Создание группы модераторов (management-команда)

В проекте есть management-команда, которая создаёт группу **«Модератор продуктов»** и назначает ей необходимые права.

### Запуск
```bash
# 1) Убедитесь, что миграции применены
python manage.py migrate

# 2) Создайте/обновите группу и права
python manage.py setup_moderators
```

После выполнения:
- в базе появится группа **«Модератор продуктов»**;
- к ней будут привязаны права `catalog.can_unpublish_product` и `catalog.delete_product`;
- добавьте нужных пользователей в группу через админку (`/admin/`) или через shell.

> Команда находится в `users/management/commands/setup_moderators.py` и может запускаться повторно — права будут актуализированы.

---

## Проверка прав в коде (сверка)

- Отмена публикации доступна пользователям, у которых есть право:
```python
request.user.has_perm("catalog.can_unpublish_product")
```

- Удаление продукта модератором (необязательно владельцем):
```python
request.user.has_perm("catalog.delete_product")
```

---

## Структура проекта (ключевые приложения)

- `catalog/` — управление продуктами (CRUD, публикация/отмена публикации).
- `users/` — кастомная модель пользователя, аутентификация, профиль.
- `config/` — настройки и корневые маршруты проекта.

---

## Полезные команды

```bash
python manage.py migrate            # применить миграции
python manage.py createsuperuser    # создать суперпользователя
python manage.py setup_moderators   # создать/обновить группу «Модератор продуктов» и назначить права
```